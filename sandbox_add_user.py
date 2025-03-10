from tkinter import *
from tkinter import ttk
import tkinter as tk
import json
from tkinter.messagebox import showerror, showwarning, showinfo
import psycopg2
# from config import host,user, password, dbname, port
import locale
import sys

current_user = {}
current_user_id = {}
new_portfolio = []

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
        print(current_user_id)
        cursor.execute('INSERT INTO user_portfolio (monkey_user_id) VALUES (%s)',(current_user_id,)) #добавляем новый порфтель в таблицу перечня клиентских портфелей
        self.connection.commit()
        cursor.execute('SELECT MAX(user_portfolio_id) FROM user_portfolio WHERE monkey_user_id = %s',(current_user_id,)) #достаем id для добавленного портфеля 
        a = cursor.fetchall()
        new_portfolio_id = int(a[0][0]) #преобразовываем полученные данные в цифру
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

    

database = Database()

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
                command=lambda: database.enter_registration_data(entry_new_user.get(),)).pack()
    
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
                                    command=self.print_selection)
            self.btns = [self.create_btn(m) for m in MODES]

            self.list.pack()
            self.print_btn.pack(fill=tk.BOTH)
            for btn in self.btns:
                btn.pack(side=tk.LEFT)

        def create_btn(self, mode):
            cmd = lambda: self.list.config(selectmode=mode)
            return tk.Button(self, command=cmd,
                            text=mode.capitalize())

        def print_selection(self):
            selection = self.list.curselection()
            global new_portfolio
            new_portfolio = [self.list.get(i) for i in selection]
            database.create_portfolio()


    if __name__ == "__main__":
        app = ListApp()
        app.mainloop()

switch_frame(login_screen)

root.mainloop()     