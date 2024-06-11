from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EthereumAddress
from .forms import CustomUserCreationForm, EthereumAddressForm
from .utils import get_ethereum_data, is_contract, get_gas_price

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
            messages.error(request, "Invalid form submission.")
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
        balance = get_ethereum_data(address.address)
        contract_status = is_contract(address.address)
        if balance is not None:
            address.balance = balance
        address.is_contract = contract_status
        address.save()

    return render(request, 'ethereum/address_list.html', {'form': form, 'addresses': addresses})

@login_required
def dashboard(request):
    gas_price = get_gas_price()
    return render(request, 'ethereum/dashboard.html', {'gas_price': gas_price})

@login_required
def home(request):
    return render(request, 'ethereum/home.html')

def set_theme(request):
    response = HttpResponse(status=200)
    theme = request.GET.get('theme', 'light')
    response.set_cookie('theme', theme)
    return response
