from django.core import validators
from django import forms

from .models import Properti

class addprop(forms.ModelForm):
    class Meta:
        model = Properti
        fields = '__all__'
        exclude = ['video']
        
