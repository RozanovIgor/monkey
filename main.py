# print("hello world")
import requests
import psycopg2


TOKEN = ""
url = f"https://api.coingecko.com/api/v3/coins/markets?x_cg_demo_api_key={TOKEN}"

headers = {"accept": "application/json"}
params = {
    "vs_currency": "eur",
    "per_page": 30
}

# response = requests.get(url, headers=headers, params=params)
# data = response.text
# with open("coins_markets.json", mode='w', encoding="utf-8") as f:
#     f.write(data)

connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = 'password',
        dbname = 'postgres',
        port = 5432
)

with connection.cursor() as cursor:
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS currencies (
            currency_id SERIAL PRIMARY KEY,
            symbol TEXT UNIQUE NOT NULL,
            name TEXT UNIQUE NOT NULL,
            image TEXT UNIQUE NOT NULL                  
            )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS currency_prices (
            currency_price_id serial primary key,
            currency_id INTEGER,
            current_price FLOAT,
            update_date TIMESTAMP,
            constraint unique_price unique (currency_id, update_date),
            FOREIGN KEY (currency_id) REFERENCES currencies(currency_id)                           
            )
        """)


connection.commit()


# https://api.coingecko.com/api/v3/ping?x_cg_demo_api_key=CG-dDR9LwhXkWppyaUki3YEWVxb
