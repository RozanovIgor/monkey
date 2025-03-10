import tkinter as tk

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


DAYS = final_text
MODES = [tk.SINGLE, tk.BROWSE, tk.MULTIPLE, tk.EXTENDED]

class ListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.list = tk.Listbox(self)
        self.list.insert(0, *DAYS)
        self.print_btn = tk.Button(self, text="Вывести выбор",
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
        print([self.list.get(i) for i in selection])


if __name__ == "__main__":
    app = ListApp()
    app.mainloop()
