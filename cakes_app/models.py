from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    name = models.CharField('Имя', max_length=256)
    phonenumber = PhoneNumberField('Телефон', region='RU')
    mail = models.CharField('Почта', max_length=256)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.name} {self.phonenumber}"


class Order(models.Model):
    CAKE_FORMS = {
        'CIRCLE': 'Круг',
        'SQUARE': 'Квадрат',
        'RECTANGLE': 'Прямоугольник',
    }
    TOPPINGS = {
        'NONE': 'Без',
        'WHITE': 'Белый соус',
        'CARAMEL': 'Карамельный',
        'MAPLE': 'Кленовый',
        'BLUEBERRIES': 'Черника',
        'MILK_CHOCOLATE': 'Молочный шоколад',
        'STRAWBERRY': 'Клубника',
    }
    BERRIES = {
        'NONE': 'Без',
        'BLACKBERRY': 'Ежевика',
        'RASPBERRY': 'Малина',
        'BLUEBERRY': 'Голубика',
        'STRAWBERRY': 'Клубника',
    }
    DECOR = {
        'NONE': 'Без',
        'PISTACHIOUS': 'Фисташки',
        'MERINGUE': 'Безе',
        'HAZELNUT': 'Фундук',
        'PECANS': 'Пекан',
        'MARSHMALLOWS': 'Маршмэллоу',
        'MARZEPAN': 'Марцепан',
    }

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент', related_name='orders')
    levels_amount = models.IntegerField("Количество уровней", validators=[MinValueValidator(0), MaxValueValidator(3)], default=1)
    form = models.CharField('Форма', choices=CAKE_FORMS, default=CAKE_FORMS['CIRCLE'], max_length=256,)
    topping = models.CharField('Топпинг', choices=TOPPINGS, default=TOPPINGS['NONE'], max_length=256,)
    berries = models.CharField('Ягоды', choices=BERRIES, default=BERRIES['NONE'], max_length=256,)
    decor = models.CharField('Декор', choices=DECOR, default=DECOR['NONE'])
    sign = models.CharField('Надпись', max_length=256)
    comment = models.TextField('Комментарий', max_length=500)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.client} {self.levels_amount}{self.form}{self.topping}"


class CakePictures(models.Model):
    name = models.CharField(max_length=256)
    picture = models.ImageField(
        upload_to='place_pictures/',
    )

    def __str__(self):
        return f'{self.name}'
