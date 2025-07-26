"""
PDF Merger.

This application allows users to select multiple PDF files, sort them by number,
merge them into a single PDF and save the result.

Author: Franck Sanchez
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PyPDF2 import PdfMerger
import webbrowser

class PDFMergerApp:
    def __init__(self, root):
        """
        Initialize the GUI layout and widgets for the PDF merger application.
        """
        self.root = root
        self.root.title("Fusionneur de fichiers PDF")

        self.pdf_paths = []

        title_frame = tk.Frame(root, bd=2, relief=tk.GROOVE, padx=10, pady=5, bg="#f0f0f0")
        title_frame.pack(pady=10, fill=tk.X)
        tk.Label(title_frame, text="Fusionneur de fichiers PDF", font=("Arial", 16, "italic"), bg="#f0f0f0").pack()

        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Choisir des fichiers PDF", command=self.select_files).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Fusionner les PDF", command=self.merge_pdfs).grid(row=0, column=1, padx=5)

        self.help_frame = tk.Frame(root)
        self.help_frame.pack(pady=5)

        self.help_button = tk.Button(self.help_frame, text="Comment fusionner les PDF ?", command=self.toggle_help)
        self.help_button.pack()

        self.help_box = tk.Label(self.help_frame, text=self.help_text(), justify=tk.LEFT, wraplength=480, fg="black", bg="#fff3cd", relief=tk.SOLID, bd=1)
        self.help_box.pack(pady=5)
        self.help_box.pack_forget()

        footer_frame = tk.Frame(root, bd=1, relief=tk.SOLID, padx=10, pady=5, bg="#f9f9f9")
        footer_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)

        content_frame = tk.Frame(footer_frame, bg="#f9f9f9")
        content_frame.pack()

        tk.Label(content_frame, text="Auteur : Franck Sanchez", font=("Arial", 10, "italic"), bg="#f9f9f9").pack(side=tk.LEFT)

        github_link = tk.Label(content_frame, text="GitHub", fg="blue", cursor="hand2",
                               font=("Arial", 10, "underline"), bg="#f9f9f9")
        github_link.pack(side=tk.LEFT, padx=(10, 5))
        github_link.bind("<Button-1>", lambda e: self.open_link("https://github.com/franck-schz"))

        barre = tk.Label(content_frame, text="|", fg="black",
                         font=("Arial", 10), bg="#f9f9f9")
        barre.pack(side=tk.LEFT)

        linkedin_link = tk.Label(content_frame, text="LinkedIn", fg="blue", cursor="hand2",
                                 font=("Arial", 10, "underline"), bg="#f9f9f9")
        linkedin_link.pack(side=tk.LEFT, padx=(5, 0))
        linkedin_link.bind("<Button-1>", lambda e: self.open_link("https://www.linkedin.com/in/franck-sanchez-77990b26b/"))
    
################################ FUNCTIONS ################################

    def help_text(self):
        """
        Returns the instructional text explaining how to use the PDF merger.
        """
        return (
            "Étapes pour fusionner les PDF :\n"
            "1. Préparez vos fichiers PDF numérotés (ex : 1.pdf, 2.pdf...).\n"
            "2. Cliquez sur \"Choisir des fichiers PDF\" et sélectionnez-les.\n"
            "3. Les fichiers seront triés automatiquement par numéro.\n"
            "4. Cliquez sur \"Fusionner les PDF\" pour créer un seul document."
        )

    def toggle_help(self):
        """
        Toggles the visibility of the help text box.
        """
        if self.help_box.winfo_ismapped():
            self.help_box.pack_forget()
        else:
            self.help_box.pack(pady=5)

    def select_files(self):
        """
        Opens a file dialog to select PDF files.
        The files are then sorted by number extracted from filenames.
        """
        paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if not paths:
            return
        self.pdf_paths = sorted(paths, key=self.extract_number)
        messagebox.showinfo("Fichiers chargés", f"{len(self.pdf_paths)} fichier(s) PDF chargé(s).")

    def extract_number(self, path):
        """
        Extracts numeric characters from a filename to use for sorting.
        """
        basename = os.path.basename(path)
        num = ''.join(filter(str.isdigit, basename))
        return int(num) if num.isdigit() else 0

    def merge_pdfs(self):
        """
        Merges the selected PDF files into a single output PDF.
        Asks the user for the destination file path.
        """
        if not self.pdf_paths:
            messagebox.showerror("Erreur", "Aucun fichier PDF sélectionné.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_path:
            return

        merger = PdfMerger()
        try:
            for path in self.pdf_paths:
                merger.append(path)
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Succès", "Les fichiers ont été fusionnés avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")

    def open_link(self, url):
        """
        Opens the specified URL in the default web browser.
        """
        webbrowser.open_new_tab(url)

###########################################################################

if __name__ == "__main__":
    root = tk.Tk()

    window_width = 600
    window_height = 400

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    app = PDFMergerApp(root)
    root.mainloop()