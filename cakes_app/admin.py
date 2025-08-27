from django.contrib import admin
from .models import Client
from .models import Order
from .models import CakePictures
from django.utils.html import format_html

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = [
        'client',
    ]
    list_display = [
        'client',
    ]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'phonenumber',
        'mail',
    ]
    list_display = [
        'name',
        'phonenumber',
        'mail',
    ]

@admin.register(CakePictures)
class CakePicturesAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]
    try:
        readonly_fields = [
            'get_picture_image',
        ]

        def get_picture_image(self, obj):
            return format_html(
                f'<img src="{obj.picture.url}" width="200" height=200 />'
            )
    except Exception as err:
        print(Exception, err)