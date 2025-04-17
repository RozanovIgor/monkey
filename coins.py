import requests
import os
from dotenv import load_dotenv

load_dotenv(".env")

TOKEN = os.getenv('COINGECKO_TOKEN')



def get_coins():
    url = f"https://api.coingecko.com/api/v3/coins/markets?x_cg_demo_api_key={TOKEN}"

    headers = {"accept": "application/json"}
    params = {
        "vs_currency": "usd",
        "per_page": 50
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data

