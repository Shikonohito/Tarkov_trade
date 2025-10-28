from tkinter import Frame, Entry, Scale, Tk, Label, Button, END


class ProductRow:
    def __init__(self, master: Frame, title: Entry, quantity: Entry,
                 min_price: Entry, max_price: Entry, slider: Scale):
        self.__master = master
        self.__title_entry = title
        self.__quantity_entry = quantity
        self.__min_price_entry = min_price
        self.__max_price_entry = max_price
        self.__slider = slider

    @property
    def frame(self):
        return self.__master

    @property
    def title_entry(self):
        return self.__title_entry

    @property
    def quantity_entry(self):
        return self.__quantity_entry

    @property
    def min_price_entry(self):
        return self.__min_price_entry

    @property
    def max_price_entry(self):
        return self.__max_price_entry

    @property
    def slider(self):
        return self.__slider

    def __eq__(self, other: Frame):
        return self.__master == other


def update_frames_row():
    row = 1
    for product_row in product_row_list:
        product_row.frame.grid(row=row, column=0, sticky="nsew", columnspan=3)
        row += 1
    product_new_frame.grid(row=row, column=0, sticky="nsew", columnspan=3)

def only_numbers(new_value):
    if new_value == "":
        return True
    return new_value.isdigit()

def on_change_slider(value):
    update_cost()

def update_cost():
    total_cost = 0
    for product_row in product_row_list:
        total_cost += product_row.slider.get() * int(product_row.quantity_entry.get())

    income = int(purchase_entry.get()) * (1 - float(tax_value_entry.get()) / 100) - total_cost
    if income < 0:
        color = "red"
    else:
        color = "green"

    cost_lbl.configure(text=total_cost, fg=color)
    income_lbl.configure(text=int(income), fg=color)


BASE_FONT = ("Arial", 18)
product_row_list: list[ProductRow] = list()

root = Tk()
root.geometry("900x780")

top_left_subframe = Frame(root)
top_left_subframe.grid(row=0, column=0, sticky="nsew")

vcmd_only_numbers = (root.register(only_numbers), "%P")

cost_purchase_lbl = Label(top_left_subframe, text="Затраты / Покупка:", font=BASE_FONT)
cost_purchase_lbl.grid(row=0, column=0, sticky="nsew", columnspan=3)

cost_lbl = Label(top_left_subframe, text="0", font=BASE_FONT, fg="green")
cost_lbl.grid(row=1, column=0, sticky="nsew")

cost_purchase_symbol_lbl = Label(top_left_subframe, text="/", font=BASE_FONT)
cost_purchase_symbol_lbl.grid(row=1, column=1, sticky="nsew")

purchase_entry = Entry(top_left_subframe, font=BASE_FONT, width=9, validate="key", validatecommand=vcmd_only_numbers)
purchase_entry.insert(0, "0")
purchase_entry.grid(row=1, column=2, sticky="nsew")
purchase_entry.bind("<FocusOut>", lambda e: update_cost())

root.grid_columnconfigure(1, weight=1)

top_right_subframe = Frame(root)
top_right_subframe.grid(row=0, column=2, sticky="nsew")

income_text_lbl = Label(top_right_subframe, text="Прибыль:", font=BASE_FONT)
income_text_lbl.grid(row=0, column=0, sticky="nsew")

income_lbl = Label(top_right_subframe, text="0", font=BASE_FONT, fg="green")
income_lbl.grid(row=0, column=1, sticky="nsew")

tax_lbl = Label(top_right_subframe, text="Налог (%): ", font=BASE_FONT)
tax_lbl.grid(row=1, column=0, sticky="nsew")

tax_value_entry = Entry(top_right_subframe, font=BASE_FONT, width=3)
tax_value_entry.insert(0, "10")
tax_value_entry.grid(row=1, column=1, sticky="nsew")
tax_value_entry.bind("<FocusOut>", lambda e: update_cost())


def create_product_row():
    def check_min(event):
        min_val = event.widget.get()
        max_val = int(product_max_entry.get())
        if not min_val:
            event.widget.delete(0, END)
            event.widget.insert(0, "0")
        elif int(min_val) > max_val:
            event.widget.delete(0, END)
            event.widget.insert(0, product_max_entry.get())

        min_val = int(product_min_entry.get())
        slider.config(from_=min_val, tickinterval=((max_val - min_val) / 10))

    def check_max(event):
        max_val = event.widget.get()
        min_val = int(product_min_entry.get())
        if not max_val or int(max_val) < min_val:
            event.widget.delete(0, END)
            event.widget.insert(0, product_min_entry.get())
        max_val = int(product_max_entry.get())
        slider.config(to=max_val, tickinterval=((max_val - min_val) / 10))

    def on_pressed(event):
        slider.focus_set()

    def delete_product_row():
        master_frame = product_del_btn.master
        product_row_list.remove(master_frame)
        master_frame.destroy()
        update_cost()


    product_frame = Frame(root, borderwidth=2, relief="groove", bg="#ddd")
    product_del_btn = Button(product_frame, text="❌", font=BASE_FONT)
    product_name_entry = Entry(product_frame, font=BASE_FONT, width=20)
    product_quantity_lbl = Label(product_frame, text="Количество:", font=BASE_FONT)

    product_quantity_entry = Entry(product_frame, font=BASE_FONT, width=3, validate="key", validatecommand=vcmd_only_numbers)
    product_quantity_entry.insert(0, "1")

    product_min_entry = Entry(product_frame, font=BASE_FONT, width=9, validate="key", validatecommand=vcmd_only_numbers)
    product_min_entry.insert(0, "0")

    slider = Scale(product_frame, from_=0, to=100, orient="horizontal", tickinterval=10, command=on_change_slider)

    product_max_entry = Entry(product_frame, font=BASE_FONT, width=9, validate="key", validatecommand=vcmd_only_numbers)
    product_max_entry.insert(0, "100")

    product_row = ProductRow(product_frame,
                             product_name_entry,
                             product_quantity_entry,
                             product_min_entry,
                             product_max_entry,
                             slider)

    product_row_list.append(product_row)

    product_frame.grid(row=1, column=0, sticky="nsew", columnspan=3)
    product_frame.grid_columnconfigure(1, weight=1)
    product_frame.grid_columnconfigure(2, weight=500)
    product_frame.grid_columnconfigure(3, weight=1)

    product_del_btn.configure(command=delete_product_row)
    product_del_btn.grid(row=0, column=0, sticky="nsew", rowspan=2)

    product_name_entry.insert(0, "Название товара")
    product_name_entry.grid(row=0, column=1, sticky="nsew", columnspan=2)

    product_quantity_lbl.grid(row=0, column=3, sticky="nsew")

    product_quantity_entry.grid(row=0, column=4, sticky="nsew")
    product_quantity_entry.bind("<FocusOut>", lambda e: update_cost())

    product_min_entry.grid(row=1, column=1, sticky="nsew")
    product_min_entry.bind("<FocusOut>", check_min)

    slider.grid(row=1, column=2, sticky="nsew", columnspan=2)
    slider.bind("<ButtonPress>", on_pressed)

    product_max_entry.grid(row=1, column=4, sticky="nsew")
    product_max_entry.bind("<FocusOut>", check_max)

    update_frames_row()
    update_cost()


product_new_frame = Frame(root, borderwidth=2, relief="groove", bg="#ddd")
product_new_frame.grid(row=2, column=0, sticky="nsew", columnspan=3)
product_new_frame.grid_columnconfigure(0, weight=1)

add_new_btn = Button(product_new_frame, text="+", font=BASE_FONT, command=create_product_row)
add_new_btn.grid(row=0, column=0, sticky="nsew")

root.mainloop()
