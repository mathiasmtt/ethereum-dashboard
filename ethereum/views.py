from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EthereumAddress
from .forms import CustomUserCreationForm, EthereumAddressForm
from .utils import get_ethereum_balance, get_ethereum_transactions, get_eth_price, get_total_supply, get_gas_price, wei_to_ether, format_number
from decimal import Decimal, InvalidOperation

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Registration successful. You are now logged in.")
                return redirect('home')
            else:
                messages.error(request, "Registration failed. Please try again.")
        else:
            messages.error(request, "Invalid form submission. Errors: " + str(form.errors))
    else:
        form = CustomUserCreationForm()
    return render(request, 'ethereum/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful. Welcome!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'ethereum/login.html', {'form': form})

@login_required

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
        balance = get_ethereum_balance(address.address)
        if balance is not None:
            try:
                address.balance = Decimal(balance) / Decimal('1000000000000000000')  # Convertir de wei a ether
            except InvalidOperation:
                address.balance = None
        address.save()

    return render(request, 'ethereum/address_list.html', {'form': form, 'addresses': addresses})

@login_required
def dashboard(request):
    gas_price = get_gas_price()
    eth_price = get_eth_price()
    total_supply = get_total_supply()
    total_supply_ether = wei_to_ether(total_supply)
    formatted_total_supply = format_number(total_supply_ether)
    return render(request, 'ethereum/dashboard.html', {
        'gas_price': gas_price,
        'eth_price': eth_price,
        'total_supply': formatted_total_supply
    })

@login_required
def home(request):
    return render(request, 'ethereum/home.html')

def set_theme(request):
    response = HttpResponse(status=200)
    theme = request.GET.get('theme', 'light')
    response.set_cookie('theme', theme)
    return response
