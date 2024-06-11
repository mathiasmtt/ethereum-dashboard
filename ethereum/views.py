from django.shortcuts import render, redirect
from .models import EthereumAddress
from .forms import EthereumAddressForm
from .utils import get_ethereum_data, is_contract, get_gas_price

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
