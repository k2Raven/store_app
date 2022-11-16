from django import forms
from django.forms import widgets
from webapp.models import CATEGORIES_CHOICES


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label="Найти")


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Наименование товара')
    description = forms.CharField(max_length=2000, required=False, label='Описание товара', widget=widgets.Textarea)
    category = forms.ChoiceField(choices=CATEGORIES_CHOICES, label='Категория')
    balance = forms.IntegerField(min_value=0, required=True, label='Остаток')
    price = forms.DecimalField(max_digits=7, decimal_places=2, label='Стоимость')
