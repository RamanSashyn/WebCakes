from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


def lk(request):
    return render(request, 'lk.html')


def lk_orders(request):
    return render(request, 'lk-order.html')
