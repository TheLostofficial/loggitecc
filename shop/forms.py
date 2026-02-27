from django import forms
from .models import Brand, Category, Format, Product


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'country']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class FormatForm(forms.ModelForm):
    class Meta:
        model = Format
        fields = ['name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'weight', 'servings', 'brand', 'category', 'format', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
        