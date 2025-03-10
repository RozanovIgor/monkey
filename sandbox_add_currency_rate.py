
import json
import psycopg2

with open('coins_markets.json','r',encoding="UTF-8") as f:
    currency_load = json.load(f)

# print(questions_load)

data_list = []
final_text = []
for d in currency_load:
    filtered_data = [d[k] for k in ("symbol","current_price","last_updated")]
    data_list.append(filtered_data)

for a in data_list:
    text_data_list = (a[0],a[1],a[2])
    final_text.append(text_data_list)

# print(data_list)
print(final_text)



connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '3t3vdeMb',
        dbname = 'postgres',
        port = 5432
)

with connection.cursor() as cursor:
        
        cursor.executemany("""INSERT INTO currency_prices (symbol,current_price,update_date) 
        VALUES (%s,%s,%s)""", (final_text)
        )
connection.commit()


# CG-dDR9LwhXkWppyaUki3YEWVxb
