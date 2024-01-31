import tkinter as tk
from tkinter import filedialog
from Bio import SeqIO
import time

class FastaViewerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("FASTA Viewer")
        # Set the window size
        width, height = 800, 600
        self.master.geometry(f"{width}x{height}")

        # Calculate the center coordinates
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set the window position to the center
        self.master.geometry(f"+{x}+{y}")

        # Color dictionary for each DNA base
        self.color_dict = {'A': 'lightblue', 'C': 'lightgreen', 'T': 'lightcoral', 'G': 'lightgoldenrodyellow'}

        # Create a Canvas widget for displaying the sequence
        self.canvas = tk.Canvas(self.master, bg="white", scrollregion=(0, 0, 800, 600))
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create a vertical scrollbar for the canvas
        v_scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')


        # Set the yscrollcommand of the canvas
        self.canvas.configure(yscrollcommand=v_scrollbar.set)

        # Create a horizontal scrollbar for the canvas
        h_scrollbar = tk.Scrollbar(self.master, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.pack(fill=tk.X)

        # Set the xscrollcommand of the canvas
        self.canvas.configure(xscrollcommand=h_scrollbar.set)

        # Create a button to load the FASTA file
        self.load_button = tk.Button(self.master, text="Load File", command=self.load_fasta_file)
        self.load_button.pack(pady=10)

    def load_fasta_file(self):
        # Open a dialog to choose a FASTA file
        fasta_file_path = filedialog.askopenfilename(title="Select a file")

        if fasta_file_path:
            # Read the FASTA file and display the sequence on the canvas
            self.display_sequence(fasta_file_path)

    def display_sequence(self, fasta_file_path):
        # Clear the canvas
        self.canvas.delete("all")

        # Read the FASTA file and get the sequence
        with open(fasta_file_path, "r") as fasta_file:
            x, y = 10, 10
            start_time = time.time()

            count = 0
            for record in SeqIO.parse(fasta_file, "fasta"):
                sequence = record.seq

                # Display each letter of the sequence on the canvas
                for letter in sequence:
                    color = self.color_dict.get(letter.upper(),'white')  # Default to white if the letter is not A, C, T, or G
                    rect_id = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill=color, outline='white')
                    text_id = self.canvas.create_text(x + 10, y + 10, text=letter, font=("Arial", 20), fill='black', anchor=tk.CENTER)
                    self.canvas.tag_bind(text_id, "<Button-1>", lambda event, letter=letter: self.on_letter_click(letter))
                    x += 20  # Adjust the spacing between letters
                y += 20  # Adjust the vertical spacing between sequences
                x = 10
                count += 1

        end_time = time.time()
        runtime = end_time - start_time
        print(f"Runtime: {runtime} seconds")
        print(f"Count: {count}")

        # Update the scrollregion after adding text items
        self.canvas.update_idletasks()
        self.update_scrollregion(None)

    def update_scrollregion(self, event):
        # Update the scrollregion based on the actual size of the canvas content
        bbox = self.canvas.bbox("all")
        self.canvas.config(scrollregion=bbox)

    def on_letter_click(self, letter):
        print(f"Selected letter: {letter}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FastaViewerApp(root)
    root.mainloop()
