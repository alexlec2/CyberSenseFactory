from tkinter import Tk, Button, PhotoImage, Label
from PIL import Image, ImageTk  # Importation pour redimensionner les images
from base import connect_to_arduino, disconnect_from_arduino, init_relay_output
from controlAiguillage import activate_relay
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Initialisation
board = None
time_sleep = 0.5  # Durée d'activation du relais (en secondes)
relays = [[13, 12], [8, 7]]  # Duo d'input pour les relais

# Fonction d'initialisation Arduino
def setup_arduino():
    global board
    name_arduino = "UNO WiFi R4"
    board = connect_to_arduino(name_arduino)
    if not board:
        print("Impossible de se connecter à l'Arduino. Le programme va se fermer.")
        exit()
    init_relay_output(board, relays)

# Fonction de redimensionnement des images
def resize_image(file_path, max_width):
    """Redimensionne une image tout en gardant ses proportions pour une largeur maximale."""
    image = Image.open(file_path)
    width, height = image.size

    if width > max_width:
        new_height = int(max_width * height / width)
        image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)

    return ImageTk.PhotoImage(image)

# Gestion d'alternance entre les relais
def toggle_relay(button, relays, images, state):
    """
    Inverse l'état de l'image du bouton et active l'alternance
    entre deux relais en fonction de l'état précédent.
    """
    # Alterne l'image
    new_state = 1 - state["image"]
    button.config(image=images[new_state])
    state["image"] = new_state

    # Active le relais alternatif
    relay_to_activate = relays[state["relay"]]
    activate_relay(board, relay_to_activate, time_sleep)
    print("Relai activé :", relay_to_activate)
    
    # Alterne entre les deux relais
    state["relay"] = 1 - state["relay"]

# Affichage de la vitesse sélectionnée avec un slider
def update_vitesse(slider, slider_value_label):
    """Mise à jour du label de vitesse en fonction de la valeur du slider."""
    vitesse = int(slider.get())  # Obtient la valeur du slider
    slider_value_label.config(text=f"Vitesse: {vitesse}%")


# Création de l'interface utilisateur
def create_ui():
    root = Tk()
    root.title("Contrôle Aiguillages")
    root.geometry("350x600")  # Taille adaptée pour les boutons et légendes

    # Chargement et redimensionnement des images
    max_width = 300
    img_position_1 = resize_image("images/position_1.png", max_width)
    img_position_2 = resize_image("images/position_2.png", max_width)
    images = [img_position_1, img_position_2]

    # États initiaux des aiguillages
    state_aiguillage_1 = {"image": 0, "relay": 0}  # image 0 = position_1, relay 0 = premier relais (13)
    state_aiguillage_2 = {"image": 0, "relay": 0}  # image 0 = position_1, relay 0 = premier relais (8)

    # Bouton pour l'aiguillage 1
    button_aiguillage_1 = Button(
        root, image=img_position_1,
        command=lambda: toggle_relay(button_aiguillage_1, relays[0], images, state_aiguillage_1)
    )
    button_aiguillage_1.pack(pady=10)

    # Légende pour l'aiguillage 1
    label_aiguillage_1 = Label(root, text="Aiguillage 1", font=("Arial", 14))
    label_aiguillage_1.pack(pady=5)

    # Bouton pour l'aiguillage 2
    button_aiguillage_2 = Button(
        root, image=img_position_1,
        command=lambda: toggle_relay(button_aiguillage_2, relays[1], images, state_aiguillage_2)
    )
    button_aiguillage_2.pack(pady=10)

    # Légende pour l'aiguillage 2
    label_aiguillage_2 = Label(root, text="Aiguillage 2", font=("Arial", 14))
    label_aiguillage_2.pack(pady=5)

    # Création du slider de vitesse
    frame_slider = ttk.Frame(root)
    frame_slider.pack(pady=10)

    # Slider avec plage de -100% à +100%
    vitesse_slider = ttk.Scale(
        frame_slider, from_=-100, to=100, value=0, length=200, orient="horizontal",
        command=lambda val: update_vitesse(vitesse_slider, slider_value_label)  # Mise à jour du label
    )
    vitesse_slider.pack()
    
    # Affichage de la valeur du slider
    slider_value_label = Label(frame_slider, text="Vitesse: 0%", font=("Arial", 14))
    slider_value_label.pack()

    # Démarrage de la boucle principale de l'interface
    root.mainloop()

# Exécution principale
if __name__ == "__main__":
    setup_arduino()  # Connexion et configuration Arduino

    print("Interface prête. Utilisez les boutons pour contrôler les aiguillages.")

    # Lance l'interface utilisateur Tkinter
    create_ui()

    # Déconnexion après fermeture de l'interface
    disconnect_from_arduino(board)
    print("Déconnexion de l'Arduino.")
