"""
Image Mosaic Generator.

This GUI application allows users to select images, arrange them in a customizable grid,
generate a mosaic and save the result as a PNG image.

Author: Franck Sanchez
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import webbrowser

class MosaicApp:
    def __init__(self, root):
        """
        Initialize the GUI and layout all widgets for the application.
        """
        self.root = root
        self.root.title("Générateur de mosaïque d'images")

        self.images = []
        self.image_paths = []

        title_frame = tk.Frame(root, bd=2, relief=tk.GROOVE, padx=10, pady=5, bg="#f0f0f0")
        title_frame.pack(pady=10, fill=tk.X)
        tk.Label(title_frame, text="Générateur de mosaïque d'images", font=("Arial", 16, "italic"), bg="#f0f0f0").pack()

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=10)

        tk.Button(self.control_frame, text="Choisir des fichiers", command=self.select_files).grid(row=0, column=0, padx=5)
        tk.Label(self.control_frame, text="Images par ligne:").grid(row=0, column=1, padx=5)
        self.cols_entry = tk.Entry(self.control_frame, width=3)
        self.cols_entry.insert(0, "3")
        self.cols_entry.grid(row=0, column=2, padx=5)

        tk.Label(self.control_frame, text="Nombre de lignes:").grid(row=0, column=3, padx=5)
        self.rows_entry = tk.Entry(self.control_frame, width=3)
        self.rows_entry.insert(0, "3")
        self.rows_entry.grid(row=0, column=4, padx=5)

        tk.Button(self.control_frame, text="Générer la mosaïque", command=self.generate_mosaic).grid(row=0, column=5, padx=5)
        self.save_btn = tk.Button(self.control_frame, text="Télécharger l'image", command=self.save_mosaic, state=tk.DISABLED)
        self.save_btn.grid(row=0, column=6, padx=5)

        self.help_frame = tk.Frame(root)
        self.help_frame.pack(pady=5)

        self.help_button = tk.Button(self.help_frame, text="Comment générer la mosaïque ?", command=self.toggle_help)
        self.help_button.pack()

        self.help_box = tk.Label(self.help_frame, text=self.help_text(), justify=tk.LEFT, wraplength=480, fg="black", bg="#fff3cd", relief=tk.SOLID, bd=1)
        self.help_box.pack(pady=5)
        self.help_box.pack_forget()

        self.canvas = tk.Canvas(root)
        self.canvas.pack(pady=10)

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
        Returns the instructional help text for generating the mosaic.
        """
        return (
            "Étapes pour générer la mosaïque :\n"
            "1. Préparez vos images numérotées de 1 à n dans un dossier.\n"
            "2. Cliquez sur \"Choisir des fichiers\" pour sélectionner vos images.\n"
            "3. Indiquez le nombre d’images par ligne et le nombre de lignes souhaité.\n"
            "4. Cliquez sur \"Générer la mosaïque\".\n"
            "5. Cliquez sur \"Télécharger l'image\" pour enregistrer la mosaïque."
        )

    def toggle_help(self):
        """
        Show or hide the help text box.
        """
        if self.help_box.winfo_ismapped():
            self.help_box.pack_forget()
        else:
            self.help_box.pack(pady=5)

    def select_files(self):
        """
        Open a file dialog to select image files and load them.
        Sorts images based on numeric values in filenames.
        """
        paths = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if not paths:
            return
        self.image_paths = sorted(paths, key=self.extract_number)
        self.images = [Image.open(path) for path in self.image_paths]
        messagebox.showinfo("Images chargées", f"{len(self.images)} image(s) chargée(s).")

    def extract_number(self, path):
        """
        Extract the numeric part of a filename for sorting purposes.
        """
        basename = os.path.basename(path)
        num = ''.join(filter(str.isdigit, basename))
        return int(num) if num.isdigit() else 0

    def generate_mosaic(self):
        """
        Generate a mosaic image using selected images based on user-defined grid size.
        """
        try:
            cols = int(self.cols_entry.get())
            rows = int(self.rows_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Entrée invalide pour les lignes/colonnes.")
            return

        n = cols * rows
        if not self.images or n == 0:
            messagebox.showerror("Erreur", "Aucune image ou disposition invalide.")
            return

        target_size = 130
        mosaic = Image.new("RGB", (cols * target_size, rows * target_size), color=(255, 255, 255))

        for i in range(min(n, len(self.images))):
            img = self.images[i].resize((target_size, target_size))
            x = (i % cols) * target_size
            y = (i // cols) * target_size
            mosaic.paste(img, (x, y))

        self.mosaic_image = mosaic
        self.display_mosaic(mosaic)
        self.save_btn.config(state=tk.NORMAL)

    def display_mosaic(self, image):
        """
        Display the generated mosaic image on the Tkinter canvas.
        """
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.config(width=image.width, height=image.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def save_mosaic(self):
        """
        Open a file dialog to save the generated mosaic image as a PNG file.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.mosaic_image.save(file_path)
            messagebox.showinfo("Succès", "Image enregistrée avec succès.")

    def open_link(self, url):
        """
        Open the given URL in the default web browser.
        """
        webbrowser.open_new_tab(url)

    def toggle_fullscreen(event=None):
        """
        Optional: Enable fullscreen mode (currently unused).
        """
        root.attributes("-fullscreen", False)

###########################################################################

if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    
    app = MosaicApp(root)
    root.mainloop()