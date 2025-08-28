from django.contrib import admin
from .models import Client, Order, Level, Form, Topping, Berry, Decor

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

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