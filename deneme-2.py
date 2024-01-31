import tkinter as tk
from tkinter import filedialog
from Bio import SeqIO

class FastaViewerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("FASTA Viewer")
        self.master.geometry("800x600")

        # Create a Text widget for displaying the sequence
        self.text_widget = tk.Text(self.master, wrap=tk.NONE, font=("Arial", 20), spacing1=2, spacing2=2, spacing3=2)
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        # Create a vertical scrollbar for the Text widget
        v_scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.text_widget.yview)
        v_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

        # Set the yscrollcommand of the Text widget
        self.text_widget.configure(yscrollcommand=v_scrollbar.set)

        # Create a horizontal scrollbar for the Text widget
        h_scrollbar = tk.Scrollbar(self.master, orient=tk.HORIZONTAL, command=self.text_widget.xview)
        h_scrollbar.pack(fill=tk.X)

        # Set the xscrollcommand of the Text widget
        self.text_widget.configure(xscrollcommand=h_scrollbar.set)

        # Create a button to load the FASTA file
        self.load_button = tk.Button(self.master, text="Load File", command=self.load_fasta_file)
        self.load_button.pack(pady=10)

    def load_fasta_file(self):
        # Open a dialog to choose a FASTA file
        fasta_file_path = filedialog.askopenfilename(title="Select a file")

        if fasta_file_path:
            # Read the FASTA file and display the sequence in the Text widget
            self.display_sequence(fasta_file_path)

    def display_sequence(self, fasta_file_path):
        # Clear the Text widget
        self.text_widget.delete("1.0", tk.END)

        # Read the FASTA file and get the sequence
        with open(fasta_file_path, "r") as fasta_file:
            for record in SeqIO.parse(fasta_file, "fasta"):
                sequence = str(record.seq)

                # Insert the sequence into the Text widget
                self.text_widget.insert(tk.END, sequence)
                self.text_widget.insert(tk.END, "\n")

        # Update the scroll region after inserting text
        self.text_widget.update_idletasks()

    def on_letter_click(self, event):
        # Get the clicked position
        index = self.text_widget.index(tk.CURRENT)
        letter = self.text_widget.get(index)

        print(f"Selected letter: {letter}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FastaViewerApp(root)
    root.mainloop()
