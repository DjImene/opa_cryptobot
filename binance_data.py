import requests
import json

# Replace these with your actual API key and secret
API_KEY = ''
API_SECRET = ''

# Define the endpoint and parameters for the API request
endpoint = 'https://api.binance.com/api/v3/ticker/24hr'  # Example endpoint for 24hr ticker price change statistics

def fetch_binance_data():
    headers = {
        'X-MBX-APIKEY': API_KEY
    }
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def save_to_json(data, filename='binance_data.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    data = fetch_binance_data()
    save_to_json(data)

if __name__ == "__main__":
    main()
