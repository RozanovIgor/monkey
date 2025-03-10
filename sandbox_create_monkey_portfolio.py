import psycopg2
import random


current_user_id = int(1)
current_portfolio_id = int(5)

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '3t3vdeMb',
        dbname = 'postgres',
        port = 5432
        )
    
    def get_current_portfolio_currency_count(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(user_portfolio_id) FROM user_portfolio_details WHERE user_portfolio_id = %s',(current_portfolio_id,)) #достаем id для добавленного портфеля 
        current_portfolio_currency_count  = int(cursor.fetchall()[0][0])
        return(current_portfolio_currency_count)
        # print(random.randint(0,current_portfolio_currency_count))

    def get_currency_count(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(symbol) FROM currency_prices') #достаем количество валют из справочника
        currency_count = int(cursor.fetchall()[0][0])
        return(currency_count)

    def get_currency_list(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT (symbol) FROM currency_prices') #достаем список валют из справочника
        currency_list = cursor.fetchall()
        return(currency_list)
    
    def add_monkey_portfolio(self,monkey_portfolio_currency_list):
        cursor = self.connection.cursor()
        cursor.executemany("""INSERT INTO monkey_portfolio_details (symbol,user_portfolio_id,quantity)
        VALUES (%s,%s,%s)""",(monkey_portfolio_currency_list)) #достаем список валют из справочника
        self.connection.commit()



database = Database()

# database.create_monkey_portfolio()
# database.get_currency_count()
# database.get_currency_list()

def generate_monkey_portfolio(current_portfolio_currency_count,currency_count,current_portfolio_id):
    a = int(0)
    monkey_portfolio_list = []
    current_portfolio_currency_count = int(current_portfolio_currency_count)
    currency_count = int(currency_count)
    while a < current_portfolio_currency_count:
            monkey_currency = random.randint(0,currency_count)
            if monkey_portfolio_list.count(monkey_currency) < 1:
                monkey_portfolio_list.append(monkey_currency)
            else: a = a - 1
            a = a + 1
    print(monkey_portfolio_list) 
    currency_list = database.get_currency_list()
    monkey_portfolio_currency_list = []
    for a in monkey_portfolio_list:
        monkey_portfolio_currency = currency_list[int(a)]
        monkey_portfolio_currency = monkey_portfolio_currency + (int(current_portfolio_id),) + (int(1),)
        monkey_portfolio_currency_list.append(monkey_portfolio_currency)
    return(monkey_portfolio_currency_list)

         

monkey_portfolio_currency_list = generate_monkey_portfolio(database.get_current_portfolio_currency_count(),database.get_currency_count(),current_portfolio_id)
print(monkey_portfolio_currency_list)
database.add_monkey_portfolio(monkey_portfolio_currency_list)








