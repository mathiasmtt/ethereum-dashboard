import requests
from django.conf import settings
from decimal import Decimal, InvalidOperation
import requests
import os
from dotenv import load_dotenv
from decimal import Decimal

def get_ethereum_data(address):
    """
    Consulta el balance de una dirección de Ethereum utilizando la API de Etherscan.
    
    :param address: Dirección de Ethereum a consultar
    :return: Balance en Ether o None si hubo un error
    """
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={settings.ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1':
        try:
            # Convertir balance de Wei a Ether
            balance = Decimal(data['result']) / Decimal(10**18)
            return balance
        except (InvalidOperation, KeyError):
            return None
    else:
        return None

def is_contract(address):
    """
    Verifica si una dirección de Ethereum es un contrato inteligente utilizando la API de Etherscan.
    
    :param address: Dirección de Ethereum a consultar
    :return: True si es un contrato inteligente, False en caso contrario
    """
    url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={settings.ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1' and len(data['result']) > 0:
        return data['result'][0]['to'] == address.lower()
    else:
        return False

def get_gas_price():
    """
    Obtiene el valor del gas de Ethereum utilizando la API de Etherscan.
    
    :return: Valor del gas en Gwei o None si hubo un error
    """
    url = f'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={settings.ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1':
        try:
            gas_price = Decimal(data['result']['ProposeGasPrice'])
            return gas_price
        except (InvalidOperation, KeyError):
            return None
    else:
        return None



load_dotenv()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

def get_ethereum_balance(address):
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['result']

def get_ethereum_transactions(address):
    url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['result']

def get_eth_price():
    url = f'https://api.etherscan.io/api?module=stats&action=ethprice&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['result']

def get_total_supply():
    url = f'https://api.etherscan.io/api?module=stats&action=ethsupply&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['result']

def get_gas_price():
    url = f'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['result']

def format_number(number):
    return '{:,}'.format(int(number))

def wei_to_ether(wei):
    return Decimal(wei) / Decimal('1000000000000000000')

def get_coingecko_data(crypto_id):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}'
    response = requests.get(url)
    data = response.json()
    return data
