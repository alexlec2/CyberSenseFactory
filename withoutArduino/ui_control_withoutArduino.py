from tkinter import Tk
from ttkbootstrap.constants import *
from tkinterElements import create_scada_frames, create_config_frame
from tkinter import Frame, Button
import json

# Initialisation
DB_PATH = "db/relays.txt"
time_sleep = 0.5  # Durée d'activation du relais (en secondes)

# Chargement des relais depuis le fichier
def load_relays(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si le fichier n'existe pas ou est corrompu, utiliser une valeur par défaut
        return [[13, 12], [8, 7], [4, 2]]

# Charger les relais depuis le fichier
relays = load_relays(DB_PATH)

def toggle_view(scada_frame, config_frame):
    """Permet de basculer entre la page de base et la page des MenuButton."""

    if scada_frame.winfo_viewable():
        scada_frame.pack_forget()
        config_frame.pack(fill='both', expand=True)
    else:
        config_frame.pack_forget()
        scada_frame.pack(fill='both', expand=True)

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
    scada_frame = Frame(root, bg="white")
    scada_frame.pack(fill='both', expand=True)

    # Appel de la fonction pour créer les frames
    create_scada_frames(scada_frame, relays, margin, time_sleep)

    # Frame pour la page avec les MenuButton
    config_frame = Frame(root, bg="white")
    config_frame.pack(fill='both', expand=True)

    board = None
    create_config_frame(config_frame, relays, DB_PATH, board)

    # Bouton pour basculer les pages
    switch_frame_button = Button(
        root, 
        text="\u2630",  # Symbole d'un menu (☰)
        bg="white",
        activebackground="lightgray",
        width=2,  # Correspond à 20 pixels environ pour la largeur en mode "grid"
        height=1,  # Pour un aspect carré
        command=lambda: toggle_view(scada_frame, config_frame)
    )
    switch_frame_button.place(relx=1, rely=0, x=-30, y=10, anchor="ne")

    config_frame.pack_forget()

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
