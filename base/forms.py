from django.forms import ModelForm
from .models import *


class ProductForm(ModelForm):
    class Meta:
        model = Sell
        fields = '__all__'
