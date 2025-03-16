# print("hello world")
import requests
import psycopg2


TOKEN = "CG-dDR9LwhXkWppyaUki3YEWVxb"
url = f"https://api.coingecko.com/api/v3/coins/markets?x_cg_demo_api_key={TOKEN}"

headers = {"accept": "application/json"}
params = {
    "vs_currency": "usd",
    "per_page": 30
}

# response = requests.get(url, headers=headers, params=params)
# data = response.text
# with open("coins_markets.json", mode='w', encoding="utf-8") as f:
#     f.write(data)

connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '3t3vdeMb',
        dbname = 'postgres',
        port = 5432
)

with connection.cursor() as cursor:
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS monkey_users (
            monkey_user_id SERIAL PRIMARY KEY,
            monkey_user_login TEXT NOT NULL)
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_portfolio (
            user_portfolio_id serial primary key,
            monkey_user_id INTEGER,
            FOREIGN KEY (monkey_user_id) REFERENCES monkey_users(monkey_user_id)                           
            )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_portfolio_details (
            user_portfolio_details_id serial primary key,
            user_portfolio_id INTEGER,
            symbol TEXT NOT NULL,
            quantity FLOAT,
            FOREIGN KEY (user_portfolio_id) REFERENCES user_portfolio(user_portfolio_id)                           
            )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS monkey_portfolio_details (
            monkey_portfolio_details_id serial primary key,
            user_portfolio_id INTEGER,
            symbol TEXT NOT NULL,
            quantity FLOAT,
            FOREIGN KEY (user_portfolio_id) REFERENCES user_portfolio(user_portfolio_id)                           
            )
        """)        
      
connection.commit()


from tkinter import *
from tkinter import ttk
import tkinter as tk
import json
from tkinter.messagebox import showerror, showwarning, showinfo
import psycopg2
import random
# from config import host,user, password, dbname, port
import locale
import sys

current_user = {}
current_user_id = {}
new_portfolio = []
current_portfolio_id = {}

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '3t3vdeMb',
        dbname = 'postgres',
        port = 5432
        )

    def enter_registration_data(self, login):
        cursor = self.connection.cursor()
        login = str(login)
        try:
            cursor.execute('INSERT INTO monkey_users (monkey_user_login) VALUES (%s)', (login,))
        except psycopg2.IntegrityError:
            showerror(title="Ошибка", message="Такой пользователь уже есть")
        self.connection.commit()

    def check_login(self, login):
        cursor = self.connection.cursor()
        cursor.execute('SELECT monkey_user_login, monkey_user_id FROM monkey_users WHERE monkey_user_login = %s ',(login,))
        user_data = cursor.fetchall()
        global current_user
        global current_user_id
        if not user_data:
            showerror(title="Ошибка", message="Неправильный логин")
            return
        else:
            showinfo(title="Правильно", message="правильный логин ")
            current_user = user_data[0][0]
            current_user_id = int(user_data[0][1])
            print(current_user,current_user_id)
            switch_frame(user_screen)

    # def get_user_portfolio(self, user_id):
        

    def create_portfolio(self):
        cursor = self.connection.cursor()
        global new_portfolio
        global current_user
        global current_user_id
        global current_portfolio_id
        print(current_user_id)
        cursor.execute('INSERT INTO user_portfolio (monkey_user_id) VALUES (%s)',(current_user_id,)) #добавляем новый порфтель в таблицу перечня клиентских портфелей
        self.connection.commit()
        cursor.execute('SELECT MAX(user_portfolio_id) FROM user_portfolio WHERE monkey_user_id = %s',(current_user_id,)) #достаем id для добавленного портфеля 
        a = cursor.fetchall()
        new_portfolio_id = int(a[0][0]) #преобразовываем полученные данные в цифру
        current_portfolio_id = new_portfolio_id
        # print(new_portfolio_id)
        load = []
        for a in new_portfolio:
             list_a = list(a)
             list_a[0]=int(new_portfolio_id)
             list_a.append(1)
             list_a = tuple(list_a)
             print(list_a)
             load.append(list_a)
        
        load = (load)
        print(load)
        cursor.executemany('INSERT INTO user_portfolio_details (user_portfolio_id, symbol, quantity) VALUES (%s,%s,%s)',(load)) #добавляем данные в новый порфтель в таблицу перечня клиентских портфелей
        self.connection.commit()

    def get_current_portfolio_currency_count(self):
        global current_portfolio_id
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

    def get_user_statistics(self):
        global current_user_id
        cursor = self.connection.cursor()
        cursor.execute("""SELECT SUM(currency_prices.current_price * user_portfolio_details.quantity)
                       FROM user_portfolio_details 
                       INNER JOIN user_portfolio ON user_portfolio_details.user_portfolio_id = user_portfolio.user_portfolio_id
                       INNER JOIN monkey_users ON user_portfolio.monkey_user_id = monkey_users.monkey_user_id
                       LEFT JOIN currency_prices ON user_portfolio_details.symbol = currency_prices.symbol
                       WHERE user_portfolio.monkey_user_id = %s""",(current_user_id,)) #выбрать все позиции портфелей клиента по его id - много SELECT?
        user_portfolio_sum = cursor.fetchall()[0][0]
        print(user_portfolio_sum)
        cursor.execute("""SELECT COUNT(user_portfolio_id)
                       FROM user_portfolio
                       WHERE user_portfolio.monkey_user_id = %s""",(current_user_id,))
        user_portfolio_count = cursor.fetchone()[0]
        print(user_portfolio_count)
        cursor.execute("""SELECT SUM(currency_prices.current_price * monkey_portfolio_details.quantity)
                       FROM monkey_portfolio_details 
                       INNER JOIN user_portfolio ON monkey_portfolio_details.user_portfolio_id = user_portfolio.user_portfolio_id
                       INNER JOIN monkey_users ON user_portfolio.monkey_user_id = monkey_users.monkey_user_id
                       LEFT JOIN currency_prices ON monkey_portfolio_details.symbol = currency_prices.symbol
                       WHERE user_portfolio.monkey_user_id = %s""",(current_user_id,))
        monkey_portfolio_value = cursor.fetchone()[0]
        print(monkey_portfolio_value)
        return(f'У вас  {user_portfolio_count} портфелей на сумму {round(user_portfolio_sum,2)} у обезъяны портфель на сумму {round(monkey_portfolio_value,2)}')
        # cursor.execute("""SELECT (symbol,current_price) FROM currency_prices""")
        # currency_price = cursor.fetchall()
        # print(currency_price)



database = Database()

def generate_monkey_portfolio(current_portfolio_currency_count,currency_count):
    global current_portfolio_id
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

root = Tk()
root.title("Вход")
root.geometry("400x400")

def switch_frame(frame):
    for widget in root.winfo_children():
        widget.destroy()
    frame()

def registration_screen():
    ttk.Label(text="Создайте логин").pack()
    entry_new_user = ttk.Entry()
    entry_new_user.pack()

    ttk.Button(text="Зарегистрироваться",
                command=lambda: database.enter_registration_data(entry_new_user.get(), switch_frame(user_screen))).pack()
    
def login_screen():
    ttk.Label(text="Введите логин").pack()
    entry_login = ttk.Entry()
    entry_login.pack()

    entry_button = ttk.Button(text="Войти",command=lambda: database.check_login(entry_login.get()))
    entry_button.pack()
    ttk.Button(text="Зарегистрироваться", command=lambda: switch_frame(registration_screen)).pack()

def user_screen():
    ttk.Label(text=f"Hello user, {current_user}").pack()
    ttk.Button(text="Создать портфель", command=lambda: switch_frame(portfolio_create_screen)).pack()
    ttk.Button(text="Посмотреть статистику ", command= lambda: switch_frame(statistics_screen)).pack()
    ttk.Button(text='Назад', command=lambda: switch_frame(login_screen)).pack()

def statistics_screen():
    ttk.Label(text=f"Hello user, {current_user}").pack()
    ttk.Label(text=f'{database.get_user_statistics()}').pack() 
    ttk.Button(text='Назад', command=lambda: switch_frame(login_screen)).pack()

def portfolio_create_screen():
    with open('coins_markets.json','r',encoding="UTF-8") as f:
        currency_load = json.load(f)

# print(questions_load)

    data_list = []
    final_text = []
    for d in currency_load:
        filtered_data = [d[k] for k in ("name","symbol")]
        data_list.append(filtered_data)

    for a in data_list:
        text_data_list = (a[0],a[1])
        final_text.append(text_data_list)


    DAYS = final_text
    MODES = [tk.MULTIPLE]

    class ListApp(tk.Tk):
        def __init__(self):
            super().__init__()
            self.list = tk.Listbox(self)
            self.list.insert(0, *DAYS)
            self.print_btn = tk.Button(self, text="Создать портфель",
                                    command=self.create_user_and_monkey_portfolios)
            self.btns = [self.create_btn(m) for m in MODES]

            self.list.pack()
            self.print_btn.pack(fill=tk.BOTH)
            for btn in self.btns:
                btn.pack(side=tk.LEFT)

        def create_btn(self, mode):
            cmd = lambda: self.list.config(selectmode=mode)
            return tk.Button(self, command=cmd,
                            text=mode.capitalize())

        def create_user_and_monkey_portfolios(self):
            selection = self.list.curselection()
            global new_portfolio
            global current_portfolio_id
            new_portfolio = [self.list.get(i) for i in selection]
            database.create_portfolio()
            monkey_portfolio_currency_list = generate_monkey_portfolio(database.get_current_portfolio_currency_count(),database.get_currency_count())
            print(monkey_portfolio_currency_list)
            database.add_monkey_portfolio(monkey_portfolio_currency_list)
            switch_frame(user_screen)


    if __name__ == "__main__":
        app = ListApp()
        app.mainloop()

switch_frame(login_screen)

root.mainloop()    








