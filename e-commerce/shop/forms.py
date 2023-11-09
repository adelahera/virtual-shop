# forms.py
from django import forms
from django.core.exceptions import ValidationError

def validate_first_letter_uppercase(value):
    if not value[0].isupper():
        raise ValidationError("First letter must be uppercase")

class ProductForm(forms.Form):

    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('jewelery', 'Jewelery'),
        ('men\'s clothing', 'Men\'s clothing'),
        ('women\'s clothing', 'Women\'s clothing')
    ]

    title = forms.CharField(label='Name', max_length=100, validators=[validate_first_letter_uppercase])
    description = forms.CharField(widget=forms.Textarea, label='Description', max_length=100)
    price = forms.FloatField(label='Price')    
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label='Category')
    image = forms.ImageField(label='Image', max_length=100, required=False)
