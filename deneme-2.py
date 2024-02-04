import tkinter as tk
from tkinter import filedialog
from Bio import SeqIO
import time
import random

class FastaViewerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("FASTA Viewer")
        self.master.geometry("1000x800")

        # Configure grid weights to make both columns expandable
        self.master.grid_rowconfigure(0, weight=1, uniform = 'a')
        self.master.grid_columnconfigure(0, weight=1, uniform = 'a')
        self.master.grid_columnconfigure(1, weight=4, uniform = 'a')

        # Create the left frame
        left_frame = tk.Frame(self.master)
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Create a Text widget for displaying sequence names
        self.seq_names_text_widget = tk.Text(left_frame, wrap=tk.NONE, font=("Courier", 20), spacing1=2, spacing2=2, spacing3=2)
        self.seq_names_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a vertical scrollbar for the sequence names Text widget
        v_scrollbar_seq_names = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.yview_text)
        v_scrollbar_seq_names.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.seq_names_text_widget.configure(yscrollcommand=v_scrollbar_seq_names.set)

        # Create a horizontal scrollbar for the Text widget
        h_scrollbar_seq_names = tk.Scrollbar(left_frame, orient=tk.HORIZONTAL, command=self.seq_names_text_widget.xview)
        h_scrollbar_seq_names.place(relx=0, rely=1, relwidth=1, anchor='sw')
        self.seq_names_text_widget.configure(xscrollcommand=h_scrollbar_seq_names.set)

        # Create the right frame
        right_frame = tk.Frame(self.master)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Create a Text widget for displaying the sequence
        self.seq_text_widget = tk.Text(right_frame, wrap=tk.NONE, font=("Courier", 20), spacing1=2, spacing2=2, spacing3=2, state="normal")
        self.seq_text_widget.pack(fill=tk.BOTH, expand=True)

        # Create a vertical scrollbar for the Text widget
        v_scrollbar = tk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.yview_text)
        v_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.seq_text_widget.configure(yscrollcommand=v_scrollbar.set)

        # Create a horizontal scrollbar for the Text widget
        h_scrollbar = tk.Scrollbar(right_frame, orient=tk.HORIZONTAL, command=self.seq_text_widget.xview)
        h_scrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')
        self.seq_text_widget.configure(xscrollcommand=h_scrollbar.set)

        # Create menu bar
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # Create a "Sequence" menu
        self.sequence_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Sequence", menu=self.sequence_menu)
        self.sequence_menu.add_command(label="Load File", command=self.load_fasta_file)

        # Dictionary to store sequences by name
        self.seq_names = []
        self.sequences = []

    def yview_text(self, *args):
        self.seq_names_text_widget.yview(*args)  # Update the sequence names Text widget
        self.seq_text_widget.yview(*args)  # Update the sequence Text widget

    def load_fasta_file(self):
        # Removes all elements from the lists
        self.seq_names.clear()
        self.sequences.clear()

        # Open a dialog to choose a FASTA file
        fasta_file_path = filedialog.askopenfilename(title="Select a file")

        if fasta_file_path:
            # Read the FASTA file and store sequences in the dictionary
            self.read_sequences(fasta_file_path)

            # Display the sequence names in the Listbox
            self.display_sequence_names()

            # Display all sequences in the Text widget
            self.display_all_sequences()

    def read_sequences(self, fasta_file_path):
        #print("read_sequences")

        # Read the FASTA file and store sequences in the dictionary
        with open(fasta_file_path, "r") as fasta_file:
            for record in SeqIO.parse(fasta_file, "fasta"):
                seq_name = record.id
                sequence = str(record.seq)
                self.seq_names.append(seq_name)
                self.sequences.append(sequence)

    def display_sequence_names(self):
        #print("display_sequence_names")

        # Clear the text widget
        self.seq_names_text_widget.configure(state="normal")
        self.seq_names_text_widget.delete("1.0", tk.END)

        # Display the sequence names in the Listbox
        self.seq_names_text_widget.insert(tk.END, "\n") # for index line

        for seq_name in self.seq_names:
            self.seq_names_text_widget.insert(tk.END, seq_name.upper())
            self.seq_names_text_widget.insert(tk.END, "\n")

        # Update the scroll region after inserting text
        self.seq_names_text_widget.update_idletasks()
        self.seq_names_text_widget.configure(state="disabled")

    def display_all_sequences(self, colored = False):
        #print("display_all_sequences")

        start_time = time.time()

        # Clear the Text widget
        self.seq_text_widget.configure(state="normal")
        self.seq_text_widget.delete("1.0", tk.END)

        # Display the sequence indices line at the top
        max_seq_length = max(len(seq) for seq in self.sequences)
        seq_indices_line = ''.join(str(i) if i % 10 == 0 and i != 0 else '.' for i in range(max_seq_length))
        self.seq_text_widget.insert(tk.END, seq_indices_line + "\n")

        color_mapping = {
            # DNA
            'A': 'green',
            'T': 'blue',
            'C': 'orange',
            'G': 'red',

            # RNA
            'U': 'purple',

            # Proteins (amino acids)
            'A': 'cyan',
            'R': 'magenta',
            'N': 'yellow',
            'D': 'brown',
            'C': 'pink',
            'E': 'olive',
            'Q': 'grey',
            'G': 'lightblue',
            'H': 'darkgreen',
            'I': 'violet',
            'L': 'darkorange',
            'K': 'darkred',
            'M': 'gold',
            'F': 'lightgreen',
            'P': 'lightpink',
            'S': 'lightcoral',
            'T': 'lightyellow',
            'W': 'lightgrey',
            'Y': 'darkcyan',
            'V': 'darkmagenta',
            '*': 'black', # Stop codon
            '-': 'grey',
        }

        for seq_name, sequence in zip(self.seq_names, self.sequences):
            # Assign unique tags to each sequence
            #fg_color = random.choice(colors)
            #bg_color = random.choice(colors)

            if colored:
                for letter in sequence:
                    # Insert the sequence into the Text widget with the configured tags
                    tag_name = f"{letter}"
                    self.seq_text_widget.tag_configure(tag_name, foreground="black", background=color_mapping[letter],
                                                       font=('Courier', 20))
                    self.seq_text_widget.insert(tk.END, letter, tag_name)
            else:
                self.seq_text_widget.insert(tk.END, sequence)
            self.seq_text_widget.insert(tk.END, "\n")

        # Update the scroll region after inserting text
        self.seq_text_widget.update_idletasks()
        self.seq_text_widget.configure(state="disabled")

        end_time = time.time()
        runtime = end_time - start_time
        print(f"Runtime: {runtime} seconds for {len(self.sequences)} seqs.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FastaViewerApp(root)
    root.mainloop()
