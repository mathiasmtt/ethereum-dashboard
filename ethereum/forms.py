# ethereum/forms.py

from django import forms
from .models import EthereumAddress

class EthereumAddressForm(forms.ModelForm):
    class Meta:
        model = EthereumAddress
        fields = ['address']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Ethereum Address'}),
        }
