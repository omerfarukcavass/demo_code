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
        self.master.grid_columnconfigure(1, weight=1, uniform = 'a')

        # Create the left frame
        left_frame = tk.Frame(self.master)
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Create a Text widget for displaying sequence names
        self.seq_names_text = tk.Text(left_frame, wrap=tk.NONE, font=("Courier", 20), spacing1=2, spacing2=2, spacing3=2,)
        self.seq_names_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a vertical scrollbar for the sequence names Text widget
        v_scrollbar_seq_names = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.seq_names_text.yview)
        v_scrollbar_seq_names.pack(side=tk.RIGHT, fill=tk.Y)
        self.seq_names_text.configure(yscrollcommand=v_scrollbar_seq_names.set)

        # Create the right frame
        right_frame = tk.Frame(self.master)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Create a Text widget for displaying the sequence
        self.text_widget = tk.Text(right_frame, wrap=tk.NONE, font=("Courier", 20), spacing1=2, spacing2=2, spacing3=2, state="normal")
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        # Create a vertical scrollbar for the Text widget
        v_scrollbar = tk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.configure(yscrollcommand=v_scrollbar.set)

        # Create a horizontal scrollbar for the Text widget
        h_scrollbar = tk.Scrollbar(right_frame, orient=tk.HORIZONTAL, command=self.text_widget.xview)
        h_scrollbar.pack(fill=tk.X)
        self.text_widget.configure(xscrollcommand=h_scrollbar.set)

        # Create menu bar
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # Create a "Sequence" menu
        self.sequence_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Sequence", menu=self.sequence_menu)
        self.sequence_menu.add_command(label="Load File", command=self.load_fasta_file)

        # Dictionary to store sequences by name
        self.sequences = {}

    def load_fasta_file(self):
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
        # Read the FASTA file and store sequences in the dictionary
        with open(fasta_file_path, "r") as fasta_file:
            for record in SeqIO.parse(fasta_file, "fasta"):
                seq_name = record.id
                sequence = str(record.seq)
                self.sequences[seq_name] = sequence

    def display_sequence_names(self):
        # Clear the Listbox
        self.seq_names_text.delete("1.0", tk.END)

        # Display the sequence names in the Listbox
        for seq_name in self.sequences:
            self.seq_names_text.insert(tk.END, seq_name.upper())
            self.seq_names_text.insert(tk.END, "\n")

        # Update the scroll region after inserting text
        self.seq_names_text.update_idletasks()
        self.seq_names_text.configure(state="disabled")

    def display_all_sequences(self, colored = False):
        start_time = time.time()

        # Clear the Text widget
        self.text_widget.delete("1.0", tk.END)

        #colors = ['red', 'blue', 'green', 'yellow']
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

        for seq_name, sequence in self.sequences.items():
            # Assign unique tags to each sequence
            #fg_color = random.choice(colors)
            #bg_color = random.choice(colors)

            if colored:
                for letter in sequence:
                    # Insert the sequence into the Text widget with the configured tags
                    tag_name = f"{letter}"
                    self.text_widget.tag_configure(tag_name, foreground="black", background=color_mapping[letter],
                                              font=('Courier', 20))
                    self.text_widget.insert(tk.END, letter, tag_name)
            else:
                self.text_widget.insert(tk.END, sequence)
            self.text_widget.insert(tk.END, "\n")

        # Update the scroll region after inserting text
        self.text_widget.update_idletasks()
        self.text_widget.configure(state="disabled")

        end_time = time.time()
        runtime = end_time - start_time
        print(f"Runtime: {runtime} seconds")


    def on_letter_click(self, event):
        # Get the clicked position
        index = self.text_widget.index(tk.CURRENT)
        letter = self.text_widget.get(index)

        print(f"Selected letter: {letter}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FastaViewerApp(root)
    root.mainloop()
