import json
import requests
from binance.client import Client
from datetime import datetime, timedelta
import pytz
import time
from tqdm import tqdm

# Fonction pour stocker les données dans le fichier JSON
def store_historical_data(file_name, candlestick_data, symbol_details):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"symbol_details": symbol_details, "data": []}
    except json.JSONDecodeError:
        print(f"Erreur de décodage JSON dans le fichier {file_name}. Réinitialisation des données.")
        data = {"symbol_details": symbol_details, "data": []}

    data['data'].extend(candlestick_data)

    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

# Fonction pour obtenir les détails du symbole via l'API CoinGecko
def get_symbol_details(binance_symbol):
    symbol_mapping = {
        "BTCUSDT": "bitcoin",
        "ETHUSDT": "ethereum",
        # Ajouter d'autres symboles plus tard
    }
    coingecko_id = symbol_mapping.get(binance_symbol, None)
    if not coingecko_id:
        print(f"Symbole Binance {binance_symbol} non trouvé dans le mapping.")
        return {
            "symbol": binance_symbol,
            "name": "",
            "market_cap": None,
            "circulating_supply": None,
            "max_supply": None
        }

    url = f'https://api.coingecko.com/api/v3/coins/{coingecko_id}'
    response = requests.get(url)
    if response.status_code == 200:
        coin_data = response.json()
        return {
            "symbol": binance_symbol,
            "name": coin_data.get('name', ''),
            "market_cap": coin_data['market_data']['market_cap'].get('usd', None),
            "circulating_supply": coin_data['market_data'].get('circulating_supply', None),
            "max_supply": coin_data['market_data'].get('max_supply', None)
        }
    else:
        return {
            "symbol": binance_symbol,
            "name": "",
            "market_cap": None,
            "circulating_supply": None,
            "max_supply": None
        }

# Fonction pour convertir les timestamps en format lisible
def convert_timestamps(data):
    for d in data:
        d['open_time'] = datetime.fromtimestamp(d['open_time'] / 1000, tz=pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
        d['close_time'] = datetime.fromtimestamp(d['close_time'] / 1000, tz=pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
    return data

# Fonction pour récupérer les données de chandeliers via l'API Binance
def fetch_data_from_binance(symbol, interval, start_time, end_time):
    client = Client()
    klines = []
    limit = 1000  # Limite maximale de données par requête

    while start_time < end_time:
        data = client.get_klines(
            symbol=symbol,
            interval=interval,
            startTime=start_time,
            endTime=min(end_time, start_time + limit * interval_to_milliseconds(interval))
        )
        if not data:
            break
        klines.extend(data)
        start_time = data[-1][0] + interval_to_milliseconds(interval)  # Passer au prochain intervalle
        print(f"Récupéré jusqu'à : {datetime.fromtimestamp(start_time / 1000, tz=pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')}")

    return klines

# Fonction pour convertir l'intervalle en millisecondes
def interval_to_milliseconds(interval):
    ms_per_unit = {
        "m": 60000,
        "h": 3600000,
        "d": 86400000,
        "w": 604800000
    }
    return int(interval[:-1]) * ms_per_unit[interval[-1]]

# Fonction principale pour récupérer les données
def fetch_data():
    # Demander à l'utilisateur de choisir un intervalle de temps
    intervals = {
        "1": "1m",    # scalping
        "2": "5m",    # scalping
        "3": "10m",   # scalping
        "4": "15m",   # scalping
        "5": "1h",    # horaire
        "6": "2h",    # horaire
        "7": "3h",    # horaire
        "8": "4h",    # horaire
        "9": "1d",    # journalier
        "10": "1w",   # hebdomadaire
        "11": "1M",   # mensuel
        "12": "3M",   # mensuel
        "13": "6M",   # mensuel
        "14": "12M"   # mensuel
    }

    print("Choisissez un intervalle de temps :")
    for key, value in intervals.items():
        print(f"{key}: {value}")
    
    while True:
        choice = input("Entrez le numéro correspondant à votre choix : ")
        if choice in intervals:
            interval = intervals[choice]
            break
        else:
            print("Choix invalide. Veuillez entrer un numéro correspondant à un intervalle de temps valide.")

    # Demander à l'utilisateur de choisir une date de début
    specific_date = input("Entrez la date de début (YYYY-MM-DD) : ")
    date_format = '%Y-%m-%d'
    
    # Convertir la date en horodatage (millisecondes)
    start_time = int(datetime.strptime(specific_date, date_format).replace(tzinfo=pytz.UTC).timestamp() * 1000)
    end_time = int(datetime.now(pytz.UTC).timestamp() * 1000)
    
    # Demander à l'utilisateur de choisir un symbole Binance
    binance_symbol = input("Entrez le symbole Binance (e.g., BTCUSDT) : ").upper()

    # Récupérer les détails du symbole via CoinGecko
    symbol_details = get_symbol_details(binance_symbol)

    # Définir le chemin spécifique pour le fichier JSON
    file_name = 'historical_data.json'
    
    print('fetch_historical_data : binance_symbol:{}, interval:{}'.format(binance_symbol, interval))

    # Récupérer les données de chandeliers via l'API Binance
    data = fetch_data_from_binance(binance_symbol, interval, start_time, end_time)
    
    # Convertir les données en format JSON compatible
    formatted_data = [
        {
            'open_time': k[0],
            'open': k[1],
            'high': k[2],
            'low': k[3],
            'close': k[4],
            'volume': k[5],
            'close_time': k[6],
            'quote_asset_volume': k[7],
            'number_of_trades': k[8],
            'taker_buy_base_asset_volume': k[9],
            'taker_buy_quote_asset_volume': k[10]
        }
        for k in data
    ]
    
    # Convertir les timestamps en format lisible
    formatted_data = convert_timestamps(formatted_data)

    # Stocker les données dans le fichier JSON
    store_historical_data(file_name, formatted_data, symbol_details)

    print("fetch_historical_data : les données historiques sont à jour")

if __name__ == '__main__':
    fetch_data()
