from django.contrib import admin
from .models import Client, Order, Level, Form, Topping, Berry, Decor, PromoCode

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phonenumber',
        'mail',
    )
    search_fields = ['name', 'phonenumber', 'mail']

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
    search_fields = [
        'client__name',
        'client__phonenumber',
        'client__mail',
        'level__name',
        'form__name',
        'topping__name',
        'sign',
        'total_price'
    ]

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
    )
    list_editable = ['price']

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
    )
    search_fields = ['name', 'price']
    list_editable = ['price']

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
    )
    search_fields = ['name', 'place']
    list_editable = ['price']

@admin.register(Berry)
class BerryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
    )
    search_fields = ['name', 'price']
    list_editable = ['price']

@admin.register(Decor)
class DecorAdmin(admin.ModelAdmin):
    pass






  
@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code',)
