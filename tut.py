import tkinter as tk
from tkinter import ttk

# this is for letter annot viewer

def on_double_click(event):
    item = tree.selection()[0]
    print("Double clicked on item:", item)

def get_all_items():
    print("============== get_all_items ==============")
    all_items = tree.get_children()
    for item_id in all_items:
        item_values = tree.item(item_id, 'values')
        print(f"Item {item_id}: {item_values}")

def add_column():
    new_column_name = entry.get()
    tree["columns"] = tree["columns"] + (new_column_name,)

    # Set heading for all columns
    for column in tree["columns"]:
        tree.heading(column, text=column)

    # Set default values for the new column for all existing items
    for item_id in tree.get_children():
        tree.set(item_id, new_column_name, "")

    get_all_items()

def delete_column():
    #last_col = tree["columns"][-1] # bunu user seçecek
    last_col = "Name" # bunu user seçecek

    column_index = tree['columns'].index(last_col)
    new_colns = tuple(item for item in tree["columns"] if item!= last_col)
    tree["columns"] = new_colns

    # Set heading for all columns
    for column in tree["columns"]:
        tree.heading(column, text=column)


    # Set default values for the new column for all existing items
    for item_id in tree.get_children():
        current_values = tree.item(item_id, 'values')
        updated_values = current_values[:column_index] + current_values[column_index + 1:]
        tree.item(item_id, values= updated_values)

    get_all_items()


root = tk.Tk()

tree = ttk.Treeview(root, show = 'headings',  columns= ("Name", "Age"))

tree.heading("Name", text="Name")
tree.heading("Age", text="Age")

# Insert some sample data
for i in range(1, 60):
    tree.insert("", "end", values=("Person {}".format(i), 25 + i))

# Bind the double-click event
tree.bind("<<TreeviewOpen>>", on_double_click)

tree.pack(expand=True, fill="both")

# Entry for adding new column
entry = tk.Entry(root)
entry.pack(pady=10)

# Button to add new column
add_button = tk.Button(root, text="Add Column", command=add_column)
add_button.pack()

# Button to delete last column
add_button = tk.Button(root, text="Delete Column", command=delete_column)
add_button.pack()


root.mainloop()
