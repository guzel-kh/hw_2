from django import forms
from django.forms import inlineformset_factory
from django.forms.fields import BooleanField

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        # fields = '__all__'
        # fields = ('name', 'description', 'preview', 'category', 'price',)
        exclude = ('owner',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        for word in self.forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Название продукта не может содержать: {self.forbidden_words}!')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        for word in self.forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Описание продукта не может содержать: {self.forbidden_words}!')

        return cleaned_data


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ('description', 'category', 'is_published',)
        # exclude = ('owner',)


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'


VersionFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)

