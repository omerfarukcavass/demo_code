import tkinter as tk
from tkinter import ttk, filedialog
from Bio import SeqIO

class FastaViewerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("FASTA Viewer")

        # Create a treeview widget to display the sequences
        self.tree = ttk.Treeview(self.master)
        self.tree["columns"] = ("Sequence ID", "Sequence")
        self.tree.heading("#0", text="Index")
        self.tree.column("#0", width=50)
        self.tree.heading("Sequence ID", text="Sequence ID")
        self.tree.column("Sequence ID", anchor=tk.W, width=150)
        self.tree.heading("Sequence", text="Sequence")
        self.tree.column("Sequence", anchor=tk.W, width=400)
        self.tree.pack(fill='both', expand=True)

        # Open a dialog to choose a FASTA file
        fasta_file_path = filedialog.askopenfilename(
            title="Select a file")

        if fasta_file_path:
            # Read the FASTA file and populate the treeview
            self.load_fasta_file(fasta_file_path)

    def load_fasta_file(self, file_path):
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Read the FASTA file and populate the treeview
        with open(file_path, "r") as fasta_file:
            for index, record in enumerate(SeqIO.parse(fasta_file, "fasta"), start=1):
                seq_id = record.id
                sequence = str(record.seq)
                self.tree.insert("", index, text=index, values=(seq_id, sequence))

if __name__ == "__main__":
    root = tk.Tk()
    app = FastaViewerApp(root)
    root.mainloop()
