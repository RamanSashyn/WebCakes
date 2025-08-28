from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Level, Form, Topping, Berry, Decor, Client, Order


def index(request):
    return render(request, 'index.html')


def lk(request):
    return render(request, 'lk.html')


def lk_orders(request):
    return render(request, 'lk-order.html')


def cake_builder_view(request: HttpRequest) -> HttpResponse:
    levels = Level.objects.all()
    forms = Form.objects.all()
    toppings = Topping.objects.all()
    berries = Berry.objects.all()
    decors = Decor.objects.all()

    if request.method == 'POST':
        level_id = request.POST.get('level')
        form_id = request.POST.get('form')
        topping_id = request.POST.get('topping')
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
            level = Level.objects.get(pk=level_id)
            total_price += level.price

        if form_id:
            form = Form.objects.get(pk=form_id)
            total_price += form.price

        if topping_id:
            topping = Topping.objects.get(pk=topping_id)
            total_price += topping.price

        for berry_id in berry_ids:
            berry = Berry.objects.get(pk=berry_id)
            total_price += berry.price

        for decor_id in decor_ids:
            decor = Decor.objects.get(pk=decor_id)
            total_price += decor.price

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

    context = {
        'levels': levels,
        'forms': forms,
        'toppings': toppings,
        'berries': berries,
        'decors': decors,
    }



    return render(request, 'index.html', context)