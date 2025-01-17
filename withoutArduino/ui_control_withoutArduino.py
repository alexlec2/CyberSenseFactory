from tkinter import Tk, IntVar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinterElements import create_frames
from tkinter import Frame, Button, Menu, Label, StringVar

# Initialisation
board = None
time_sleep = 0.5  # Durée d'activation du relais (en secondes)
relays = [[13, 12], [8, 7], [4, 2]]  # Duo d'input pour les relais

def toggle_view(scada_frame, buttons_frame):
    """Permet de basculer entre la page de base et la page des MenuButton."""

    if scada_frame.winfo_viewable():
        scada_frame.pack_forget()
        buttons_frame.pack(fill='both', expand=True)
    else:
        buttons_frame.pack_forget()
        scada_frame.pack(fill='both', expand=True)

def update_label(label, value):
    print(value)
    label.config(text=f'Relai {value}')

# Création de l'interface utilisateur
def create_ui():
    root = Tk()
    root.title("Scada CyberSense Factory")
    root.geometry("800x800")

    # Configuration de la grille
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.columnconfigure(0, weight=1, minsize=800)  # Limite de la largeur maximale

    # Marges et padding
    margin = 20

    # Frame de la page de base
    scada_frame = Frame(root)
    scada_frame.pack(fill='both', expand=True)

    # Appel de la fonction pour créer les frames
    create_frames(scada_frame, relays, margin, time_sleep)

    # Frame pour la page avec les MenuButton
    buttons_frame = Frame(root, bg="white", height=800, width=800)
    buttons_frame.pack(fill='both', expand=True)

    list_relays_elements = ["A1 Relai 1", "A1 Relai 2", "A2 Relai 1", "A2 Relai 2", "Train Relai 1", "Train Relai 2"]
    styles = ["primary", "primary", "info", "info", "danger", "danger"]
    default_values = [13, 12, 8, 7, 4, 2]

    for index, option in enumerate(list_relays_elements):
        # Créer un MenuButton pour chaque option
        mb = ttk.Menubutton(buttons_frame, text=option, bootstyle=styles[index])
        mb.pack(pady=5, padx=20, anchor="center")

        # Associer un label à chaque MenuButton
        label = Label(buttons_frame, text=f"Relai {default_values[index]}", font=("Arial", 12))
        label.pack(pady=2)

        # Ajouter un menu déroulant pour changer la valeur
        menu = Menu(mb, tearoff=0)
        default_value = IntVar(value=default_values[index])

        def make_update_function(lbl, var):
            def update_label():
                lbl.config(text=f"Relai {var.get()}")
            return update_label

        for value in default_values:
            menu.add_radiobutton(label=str(value), variable=default_value, value=value, command=make_update_function(label, default_value))

        mb["menu"] = menu

    # Bouton pour basculer les pages
    switch_button = Button(
        root, 
        text="\u2630",  # Symbole d'un menu (☰)
        bg="white",
        activebackground="lightgray",
        width=2,  # Correspond à 20 pixels environ pour la largeur en mode "grid"
        height=1,  # Pour un aspect carré
        command=lambda: toggle_view(scada_frame, buttons_frame)
    )
    switch_button.place(relx=1, rely=0, x=-30, y=10, anchor="ne")

    scada_frame.pack_forget()

    # Lancement de l'application
    root.mainloop()

# Exécution principale
if __name__ == "__main__":
    # setup_arduino()  # Connexion et configuration Arduino

    print("Interface prête. Utilisez les boutons pour contrôler les aiguillages.")

    # Lance l'interface utilisateur Tkinter
    create_ui()

    # Déconnexion après fermeture de l'interface
    # disconnect_from_arduino(board)
    print("Déconnexion de l'Arduino.")
