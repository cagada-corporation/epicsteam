from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Product


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    is_seller = forms.BooleanField(required=False)

    class Meta:
        model = User

        fields = (
            'username',
            'email',
            'is_seller',
            'password1',
            'password2'
        )


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'name',
            'description',
            'image',
            'price',
            'stock',
            'platform',
            'categories'
        ]

        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }