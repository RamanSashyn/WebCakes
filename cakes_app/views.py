import re
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Level, Form, Topping, Berry, Decor, Client, Order
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PhoneLoginForm, ProfileForm
from django.db import transaction



def index(request: HttpRequest) -> HttpResponse:
    levels = Level.objects.all()
    forms = Form.objects.all()
    toppings = Topping.objects.all()
    berries = Berry.objects.all()
    decors = Decor.objects.all()

    show_login = request.session.pop('show_login_modal', False)

    if request.method == 'POST':
        level_id = request.POST.get('level')
        form_id = request.POST.get('form')
        topping_id = request.POST.get('topping')
        berry_ids = request.POST.getlist('berries')
        decor_ids = request.POST.getlist('decor')
        words = request.POST.get('words')
        comment = request.POST.get('comment')

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        date = request.POST.get('date')
        time = request.POST.get('time')
        deliv_comment = request.POST.get('deliv_comment')

        total_price = 0

        if level_id:
            total_price += Level.objects.get(pk=level_id).price
        if form_id:
            total_price += Form.objects.get(pk=form_id).price
        if topping_id:
            total_price += Topping.objects.get(pk=topping_id).price
        for berry_id in berry_ids:
            total_price += Berry.objects.get(pk=berry_id).price
        for decor_id in decor_ids:
            total_price += Decor.objects.get(pk=decor_id).price

        client, created = Client.objects.get_or_create(
            phonenumber=phone,
            defaults={
                'name': name,
                'mail': email
            }
        )
        new_order = Order.objects.create(
            client=client,
            level=Level.objects.get(pk=level_id),
            form=Form.objects.get(pk=form_id),
            topping=Topping.objects.get(pk=topping_id),
            sign=words,
            comment=comment,
            total_price=total_price,
        )
        new_order.berries.set(Berry.objects.filter(pk__in=berry_ids))
        new_order.decor.set(Decor.objects.filter(pk__in=decor_ids))

        return redirect('index')

    context = {
        'levels': levels,
        'forms': forms,
        'toppings': toppings,
        'berries': berries,
        'decors': decors,
        'login_form': PhoneLoginForm(),
        'show_login_modal': show_login,
    }

    return render(request, 'index.html', context)


@login_required
def lk_view(request):
    return render(request, 'lk.html')


def login_view(request):
    if request.method != 'POST':
        return redirect('index')

    form = PhoneLoginForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Исправьте ошибки формы')
        request.session['show_login_modal'] = True
        return redirect('index')

    raw_phone = form.cleaned_data['phone']
    password  = form.cleaned_data['password']

    for uname in phone_candidates(raw_phone):
        user = authenticate(request, username=uname, password=password)
        if user:
            login(request, user)
            return redirect('lk')

    if find_user_by_candidates(raw_phone):
        messages.error(request, 'Неверный телефон или пароль')
        request.session['show_login_modal'] = True
        return redirect('index')

    username = normalize_plus7(raw_phone)
    user = User.objects.create_user(username=username, password=password)

    try:
        client, created = Client.objects.get_or_create(
            phonenumber=username,
            defaults={'name': username}
        )
        if hasattr(client, 'user') and not client.user:
            client.user = user
            client.save()
    except Exception:
        pass

    login(request, user)
    return redirect('lk')


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')



@login_required
def lk(request):
    user = request.user
    client = get_client_for_user(user)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            name  = form.cleaned_data['name'].strip()
            phone = normalize_plus7(form.cleaned_data['phone'])
            email = form.cleaned_data['email'].strip()

            # телефон (username) должен быть уникальным
            if User.objects.exclude(pk=user.pk).filter(username=phone).exists():
                messages.error(request, 'Этот телефон уже используется другим аккаунтом.')
            else:
                with transaction.atomic():
                    # обновляем User
                    user.first_name = name
                    user.email = email
                    user.username = phone
                    user.save(update_fields=['first_name', 'email', 'username'])

                    # обновляем Client
                    client.name = name
                    client.phonenumber = phone
                    client.mail = email
                    client.save(update_fields=['name', 'phonenumber', 'mail'])

                messages.success(request, 'Данные профиля обновлены.')
                return redirect('lk')
    else:
        initial = {
            'name':  user.first_name or client.name or '',
            'phone': client.phonenumber or user.username or '',
            'email': user.email or client.mail or '',
        }
        form = ProfileForm(initial=initial)

    orders = Order.objects.filter(client=client).select_related(
        'level', 'form', 'topping'
    ).prefetch_related('berries', 'decor')

    return render(request, 'lk.html', {'form': form, 'orders': orders})



def get_client_for_user(user):
    """Вернуть/создать клиента для текущего пользователя."""
    try:
        Client._meta.get_field('user')
        c = Client.objects.filter(user=user).first()
        if c:
            return c
    except Exception:
        c = None

    c = Client.objects.filter(phonenumber=user.username).first()
    if c:
        try:
            if hasattr(c, 'user') and not c.user_id:
                c.user = user
                c.save(update_fields=['user'])
        except Exception:
            pass
        return c

    c = Client(
        name=user.first_name or '',
        phonenumber=user.username,
        mail=user.email or '',
    )
    try:
        Client._meta.get_field('user')
        c.user = user
    except Exception:
        pass
    c.save()
    return c


def lk_orders(request):
    return render(request, 'lk-order.html')


def phone_candidates(raw: str):
    """Возможные варианты username по введённому телефону."""
    d = re.sub(r'\D', '', raw or '')
    if not d:
        return []
    cand = [d]  # 7922...
    d7 = ('7'+d[1:]) if d.startswith('8') else (d if d.startswith('7') else '7'+d)
    cand += [d7, '+'+d7]  # 7..., +7...
    out, seen = [], set()
    for x in cand:
        if x not in seen:
            out.append(x); seen.add(x)
    return out

def normalize_plus7(raw: str) -> str:
    d = re.sub(r'\D', '', raw or '')
    if not d: return ''
    if d.startswith('8'):
        d = '7'+d[1:]
    if not d.startswith('7'):
        d = '7'+d
    return '+'+d


def find_user_by_candidates(raw: str):
    """Есть ли пользователь с таким телефоном (в любом из допустимых форматов)."""
    for uname in phone_candidates(raw):
        u = User.objects.filter(username=uname).first()
        if u:
            return u
    return None


# def cake_builder_view(request: HttpRequest) -> HttpResponse:
#     levels = Level.objects.all()
#     forms = Form.objects.all()
#     toppings = Topping.objects.all()
#     berries = Berry.objects.all()
#     decors = Decor.objects.all()
#
#     if request.method == 'POST':
#         level_id = request.POST.get('level')
#         form_id = request.POST.get('form')
#         topping_id = request.POST.get('topping')
#         form_id = request.POST.get('form')
#         topping_id = request.POST.get('topping')
#         berry_ids = request.POST.getlist('berries')
#         decor_ids = request.POST.getlist('decor')
#         words = request.POST.get('words')
#         comment = request.POST.get('comment')
#
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         address = request.POST.get('address')
#         date = request.POST.get('date')
#         time = request.POST.get('time')
#         deliv_comment = request.POST.get('deliv_comment')
#
#         total_price = 0
#
#         if level_id:
#             level = Level.objects.get(pk=level_id)
#             total_price += level.price
#
#         if form_id:
#             form = Form.objects.get(pk=form_id)
#             total_price += form.price
#
#         if topping_id:
#             topping = Topping.objects.get(pk=topping_id)
#             total_price += topping.price
#
#         for berry_id in berry_ids:
#             berry = Berry.objects.get(pk=berry_id)
#             total_price += berry.price
#
#         for decor_id in decor_ids:
#             decor = Decor.objects.get(pk=decor_id)
#             total_price += decor.price
#
#         client, created = Client.objects.get_or_create(
#             phonenumber=phone,
#             defaults={
#                 'name': name,
#                 'mail': email
#             }
#         )
#         new_order = Order.objects.create(
#             client=client,
#             level=Level.objects.get(pk=level_id),
#             form=Form.objects.get(pk=form_id),
#             topping=Topping.objects.get(pk=topping_id),
#             sign=words,
#             comment=comment,
#             total_price=total_price,
#         )
#
#         new_order.berries.set(Berry.objects.filter(pk__in=berry_ids))
#         new_order.decor.set(Decor.objects.filter(pk__in=decor_ids))
#
#     context = {
#         'levels': levels,
#         'forms': forms,
#         'toppings': toppings,
#         'berries': berries,
#         'decors': decors,
#     }
#
#
#
#     return render(request, 'index.html', context)