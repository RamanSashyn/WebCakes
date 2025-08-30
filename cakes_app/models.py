from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='client',
        verbose_name='Пользователь',
        null=True, blank=True
    )
    name = models.CharField('Имя', max_length=256, blank=True)
    phonenumber = PhoneNumberField('Телефон', region='RU', unique=True)
    mail = models.CharField('Почта', max_length=256, blank=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.name or self.user or ''} {self.phonenumber}"


class Level(models.Model):
    name = models.CharField('Название', max_length=256)
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )

    class Meta:
        verbose_name = 'Уровень'
        verbose_name_plural = 'Уровни'

    def __str__(self):
        return self.name


class Form(models.Model):
    name = models.CharField('Название', max_length=256)
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )

    class Meta:
        verbose_name = 'Форма'
        verbose_name_plural = 'Формы'

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField('Название', max_length=256)
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )

    class Meta:
        verbose_name = 'Топпинг'
        verbose_name_plural = 'Топпинги'

    def __str__(self):
        return self.name


class Berry(models.Model):
    name = models.CharField('Название', max_length=256)
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )

    class Meta:
        verbose_name = 'Ягода'
        verbose_name_plural = 'Ягоды'

    def __str__(self):
        return self.name


class Decor(models.Model):
    name = models.CharField('Название', max_length=256)
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )

    class Meta:
        verbose_name = 'Декор'
        verbose_name_plural = 'Декоры'

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент', related_name='orders')
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, verbose_name='Количество уровней', related_name='orders')
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True, verbose_name='Форма', related_name='orders')
    topping = models.ForeignKey(Topping, on_delete=models.SET_NULL, null=True, verbose_name='Топпинг', related_name='orders')
    berries = models.ManyToManyField(Berry, blank=True, verbose_name='Ягоды', related_name='orders')
    decor = models.ManyToManyField(Decor,  blank=True, verbose_name='Декор', related_name='orders')
    sign = models.CharField('Надпись', max_length=256, blank=True)
    comment = models.TextField('Комментарий', max_length=500, blank=True)
    total_price = models.DecimalField(
        'Итоговая стоимость',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        default=0.00
    )
    promo_code = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ {self.pk}"


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="Промокод")
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Скидка (%)")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.code