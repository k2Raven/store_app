from django.db import models

CATEGORIES_CHOICES = [("other", "Разное"), ("electronics", "Электроника"), ("books", "Книги"),
                      ("stationery", "Канцтовары")]


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Наименование товара')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание товара')
    category = models.CharField(max_length=50, choices=CATEGORIES_CHOICES, default=CATEGORIES_CHOICES[0][0],
                                verbose_name="Категория")
    balance = models.PositiveIntegerField(verbose_name='Остаток')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Стоимость")

    def __str__(self):
        return f'{self.id}. {self.name}'
