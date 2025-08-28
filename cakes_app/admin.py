from django.contrib import admin
from .models import Client, Order, Level, Form, Topping, Berry, Decor

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'client',
        'level',
        'form',
        'topping',
        'sign',
        'total_price',
    )
    list_filter = ('level', 'form', 'topping')

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    pass

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    pass

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    pass

@admin.register(Berry)
class BerryAdmin(admin.ModelAdmin):
    pass

@admin.register(Decor)
class DecorAdmin(admin.ModelAdmin):
    pass