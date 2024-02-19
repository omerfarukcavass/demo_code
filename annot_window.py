import tkinter as tk
from tkinter import ttk

# this is for annot viewer


def get_all_items():
    print("============== get_all_items ==============")
    all_items = tree.get_children()
    for item_id in all_items[:3]:
        item_values = tree.item(item_id, 'values')
        print(f"Item {item_id}: {item_values}")


def add_column():
    new_column_name = entry.get()

    # Preserve current column headers and their settings
    new_columns = [new_column_name]
    current_columns = list(tree['columns'])
    current_columns = {key: tree.heading(key) for key in current_columns} # get heading info

    # Update with new columns
    tree['columns'] = list(current_columns.keys()) + list(new_columns)
    for key in new_columns:
        tree.heading(key, text=key)

    # Set saved column values for the already existing columns
    for key in current_columns:
        # State is not valid to set with heading
        state = current_columns[key].pop('state')
        tree.heading(key, **current_columns[key])

    # Set default values for the new column for all existing items
    for item_id in tree.get_children():
        tree.set(item_id, new_column_name, "")

    get_all_items()


def delete_column():
    col_name = tree["columns"][-1] # bunu user seçecek
    column_index = tree['columns'].index(col_name)

    current_columns = list(tree['columns'])
    current_columns = {key: tree.heading(key) for key in current_columns if key != col_name} # get heading info

    tree["columns"] = list(current_columns.keys())

    # Set saved column values for the already existing columns
    for key in current_columns:
        # State is not valid to set with heading
        state = current_columns[key].pop('state')
        tree.heading(key, **current_columns[key])

    # Set default values for the new column for all existing items
    for item_id in tree.get_children():
        current_values = tree.item(item_id, 'values')
        updated_values = current_values[:column_index] + current_values[column_index + 1:]
        tree.item(item_id, values= updated_values)

    get_all_items()


def on_configure(event):
    # Adjust column widths when the window size changes
    for column in tree['columns']:
        tree.column(column, width=200, minwidth=100)


root = tk.Tk()

# Notebook widget
notebook = ttk.Notebook(root)

# tab 1
tab1 = ttk.Frame(notebook)
tree = ttk.Treeview(tab1, show = 'headings',  selectmode='browse', columns= ("Name", "Age", "Salary"))

tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Salary", text="Salary")
tree.column("Name", minwidth=100)
tree.column("Age", minwidth=100)
tree.column("Salary", minwidth=100)


# Insert some sample data
for i in range(1, 60):
    tree.insert("", "end", values=("Person {}".format(i), 25 + i, 1000 * i))

tree.pack(expand=True, fill="both")

# Create vertical scrollbar
vscrollbar = ttk.Scrollbar(tab1, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vscrollbar.set)
vscrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

# Create horizontal scrollbar
hscrollbar = ttk.Scrollbar(tab1, orient="horizontal", command=tree.xview)
tree.configure(xscrollcommand=hscrollbar.set)
hscrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')

tab2 = ttk.Frame(notebook)
notebook.add(tab1, text='Tab 1')
notebook.add(tab2, text='Tab 2')
notebook.pack(fill='both', expand=True)


# Entry for adding new column
entry = tk.Entry(root)
entry.pack(pady=10)

# Button to add new column
add_button = tk.Button(root, text="Add Column", command=add_column)
add_button.pack()

# Button to delete last column
delete_button = tk.Button(root, text="Delete Column", command=delete_column)
delete_button.pack()

# Bind the Configure event to adjust column widths
tree.bind("<Configure>", on_configure)

root.mainloop()
