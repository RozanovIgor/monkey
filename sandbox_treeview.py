
import csv
import tkinter as tk
import tkinter.ttk as ttk


import json

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

class App(tk.Tk):
    def __init__(self, path):
        super().__init__()
        self.title("Ttk Treeview")

        columns = ("#1", "#2", "#3")
        self.tree = ttk.Treeview(self, show="headings", columns=columns)
        self.tree.heading("#1", text="Фамилия")
        self.tree.heading("#2", text="Имя")
        self.tree.heading("#3", text="Почта")
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)

        with open("../lesson_13/contacts.csv", newline="") as f:
            for contact in csv.reader(f):
                self.tree.insert("", tk.END, values=contact)
        self.tree.bind("<<TreeviewSelect>>", self.print_selection)

        self.tree.grid(row=0, column=0)
        ysb.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def print_selection(self, event):
        for selection in self.tree.selection():
            item = self.tree.item(selection)
            last_name, first_name, email = item["values"][0:3]
            text = "Выбор: {}, {} <{}>"
            print(text.format(last_name, first_name, email))

if __name__ == "__main__":
    app = App(path=".")
    app.mainloop()