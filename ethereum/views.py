from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect



from django.shortcuts import render, redirect
from .models import EthereumAddress
from .forms import EthereumAddressForm
from .utils import get_ethereum_data, is_contract, get_gas_price

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'ethereum/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'ethereum/login.html', {'form': form})

def address_list(request):
    if request.method == 'POST':
        form = EthereumAddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('address_list')
    else:
        form = EthereumAddressForm()

    addresses = EthereumAddress.objects.all()
    for address in addresses:
        balance = get_ethereum_data(address.address)
        contract_status = is_contract(address.address)
        if balance is not None:
            address.balance = balance
        address.is_contract = contract_status
        address.save()

    return render(request, 'ethereum/address_list.html', {'form': form, 'addresses': addresses})

def dashboard(request):
    gas_price = get_gas_price()
    return render(request, 'ethereum/dashboard.html', {'gas_price': gas_price})

def home(request):
    return render(request, 'ethereum/home.html')
