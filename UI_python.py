import tkinter as tk
from tkinter import messagebox

def on_button_click():
    messagebox.showinfo("Message", "Bonjour, Tkinter fonctionne bien !")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Fenêtre Tkinter")
root.geometry("300x200")

# Création d'une étiquette
label = tk.Label(root, text="Bienvenue sur Tkinter !", font=("Arial", 14))
label.pack(pady=20)

# Création d'un bouton
button = tk.Button(root, text="Cliquez-moi", command=on_button_click)
button.pack(pady=10)

# Boucle principale pour afficher la fenêtre
root.mainloop()
