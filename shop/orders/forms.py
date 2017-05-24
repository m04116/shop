from django import forms


class CartContactForm(forms.Form):
    name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
