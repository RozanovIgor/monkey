import os

from coins import get_coins
from db import Database

from dotenv import load_dotenv

load_dotenv()


coins = get_coins()


db = Database(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"),
              password=os.getenv("DB_PASS"), user=os.getenv("DB_USER"))


# Добавление данных
# db.add_coins(coins)
# db.add_market_data(coins)


import tkinter as tk
from tkinter import messagebox


class Interface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Авторизация")
        self.root.geometry("500x500")

        self.switch_frame(self.show_login_window)
        self.root.mainloop()


    def switch_frame(self, frame, title=None):
        for widget in self.root.winfo_children():
            widget.destroy()

        if title:
            self.root.title(title)
        frame()

    def show_login_window(self):
        # Метка и поле ввода логина
        label_username = tk.Label(self.root, text="Логин:")
        label_username.pack(pady=(20, 0))
        entry_username = tk.Entry(self.root)
        entry_username.pack()

        # Метка и поле ввода пароля
        label_password = tk.Label(self.root, text="Пароль:")
        label_password.pack(pady=(10, 0))
        entry_password = tk.Entry(self.root, show="*")
        entry_password.pack()

        # Кнопка входа
        btn_login = tk.Button(self.root, text="Войти", command=lambda: self.login(username=entry_username.get(), password=entry_password.get()))
        btn_login.pack(pady=(15, 5))

        # Кнопка регистрации
        btn_register = tk.Button(self.root, text="Зарегистрироваться", command=lambda: self.switch_frame(self.show_sign_window, "Создание"))
        btn_register.pack()


    def show_sign_window(self):
        label_username = tk.Label(self.root, text="Логин:")
        label_username.pack(pady=(20, 0))
        entry_username = tk.Entry(self.root)
        entry_username.pack()

        # Метка и поле ввода пароля
        label_password = tk.Label(self.root, text="Пароль:")
        label_password.pack(pady=(10, 0))
        entry_password = tk.Entry(self.root, show="*")
        entry_password.pack()

        # Кнопка входа
        btn_sign = tk.Button(self.root, text="Создать аккаунт",
                              command=lambda: self.register(username=entry_username.get(), password=entry_password.get()))
        btn_sign.pack(pady=(15, 5))


    def show_product_selection(self):
        all_products = db.get_coins()
        filtered_products = all_products.copy()

        def update_listbox(filter_text=""):
            listbox.delete(0, tk.END)
            nonlocal filtered_products
            filtered_products = [item for item in all_products if filter_text.lower() in item.lower()]
            for item in filtered_products:
                listbox.insert(tk.END, item)
            update_counter()

        def update_counter(event=None):
            selected = listbox.curselection()
            counter_label.config(text=f"Выбрано: {len(selected)}")

        def continue_action():
            selected_indices = listbox.curselection()
            selected_items = [filtered_products[i] for i in selected_indices]
            messagebox.showinfo("Вы выбрали", ", ".join(selected_items))

        def clear_selection():
            listbox.selection_clear(0, tk.END)
            update_counter()

        def on_search_change(*args):
            text = search_var.get()
            update_listbox(text)

        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title("Выбор продуктов")

        # Поисковое поле
        search_var = tk.StringVar()
        search_var.trace_add("write", on_search_change)
        search_entry = tk.Entry(self.root, textvariable=search_var, width=40)
        search_entry.pack(pady=(10, 5))
        search_entry.insert(0, "Поиск...")

        def clear_placeholder(event):
            if search_entry.get() == "Поиск...":
                search_entry.delete(0, tk.END)

        search_entry.bind("<FocusIn>", clear_placeholder)

        # Список продуктов
        listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=40, height=10)
        listbox.pack()
        listbox.bind("<<ListboxSelect>>", update_counter)

        # Счётчик
        counter_label = tk.Label(self.root, text="Выбрано: 0")
        counter_label.pack(pady=5)

        # Кнопки
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        clear_button = tk.Button(button_frame, text="Снять выбор", command=clear_selection)
        clear_button.grid(row=0, column=0, padx=10)

        continue_button = tk.Button(button_frame, text="Продолжить", command=continue_action)
        continue_button.grid(row=0, column=1, padx=10)

        update_listbox()  # Изначально загрузить весь список

    def login(self, username, password):
        if db.check_user_exists(username, password):
            self.switch_frame(self.show_product_selection)
        else:
            messagebox.showerror("Вход", "no-no-no...")

    def register(self, username, password):
        db.add_user(username, password)
        messagebox.showinfo("Вход", "Success created")
        self.switch_frame(self.show_login_window)



window = Interface()