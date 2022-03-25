from django.core import validators
from django import forms
from matplotlib import widgets
from .models import Properti

class addprop(forms.ModelForm):
    class Meta:
        model = Properti
        fields = '__all__'
        exclude = ['video']
        widgets={
            '__all__': forms.TextInput(attrs={'class':'form-control'}),
        }
