from tkinter import Tk, Button, Label
from PIL import Image, ImageTk  # Importation pour redimensionner les images
from controlAiguillage_withoutArduino import activate_relay
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Initialisation
board = None
time_sleep = 0.5  # Durée d'activation du relais (en secondes)
relays = [[13, 12], [8, 7], [4, 2]]  # Duo d'input pour les relais
speed_status = 0
cycle_vitesse_states = [0, 10, 0, -10]
current_cycle_index = 0


# Fonction de redimensionnement des images
def resize_image(file_path, max_width):
    """Redimensionne une image tout en gardant ses proportions pour une largeur maximale."""
    image = Image.open(file_path)
    width, height = image.size

    if width > max_width:
        new_height = int(max_width * height / width)
        image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)

    return ImageTk.PhotoImage(image)

# Affichage de la vitesse sélectionnée avec un slider
def update_vitesse(slider, slider_value_label):
    """Mise à jour du label de vitesse en fonction de la valeur du slider + activate relay of vitesse"""
    global speed_status

    vitesse = int(slider.get())*10  # Obtient la valeur du slider
    slider_value_label.config(text=f"Vitesse: {vitesse}")

    if vitesse == 10 and speed_status != 10:
        # board.digital[relays[2][1]].write(0)
        print(f"Activation du relais {relays[2][1]}.")
        # board.digital[relays[2][0]].write(1)
        print(f"Le relais {relays[2][0]} est à 0.")
        print("Le train avance")
        speed_status = 10

    elif vitesse == -10 and speed_status != -10:
        # board.digital[relays[2][0]].write(0)
        print(f"Activation du relais {relays[2][0]}.")
        # board.digital[relays[2][1]].write(1)
        print(f"Le relai {relays[2][1]} est à 0.")
        print("Le train recule")
        speed_status = -10

    elif vitesse == 0 and speed_status != 0:
        # board.digital[relays[2][1]].write(0)
        # board.digital[relays[2][0]].write(0)
        print(f"Le relais {relays[2][0]} est à 0.")
        print(f"Le relais {relays[2][1]} est à 0.")
        print("Le train est à l'arrêt")
        speed_status = 0

    return speed_status

def bouton_clicked(button, relays, images, state):
    """Fonction appelée lorsqu'un bouton est cliqué (ou pressé avec Enter)."""
    # Alterne l'image entre position_1 et position_2
    new_state = 1 - state["image"]
    button.config(image=images[new_state])  # Met à jour l'image sur le bouton
    state["image"] = new_state

    # Active le relais correspondant
    relay_to_activate = relays[state["relay"]]
    activate_relay(board, relay_to_activate, time_sleep)
    print(f"Relais activé : {relay_to_activate}")

    # Alterne entre les deux relais
    state["relay"] = 1 - state["relay"]

# Création de l'interface utilisateur
def create_ui():
    global vitesse_slider  # Rendre la variable disponible dans la fonction d'événement
    global slider_value_label, current_cycle_index, cycle_vitesse_states

    root = Tk()
    root.title("Contrôle Aiguillages")
    root.geometry("350x600")  # Taille adaptée pour les boutons et légendes


    # Chargement et redimensionnement des images
    max_width = 300
    img_position_1 = resize_image("../images/position_1.png", max_width)
    img_position_2 = resize_image("../images/position_2.png", max_width)
    images = [img_position_1, img_position_2]

    # États initiaux des aiguillages
    state_aiguillage_1 = {"image": 0, "relay": 0}  # image 0 = position_1, relay 0 = premier relais (13)
    state_aiguillage_2 = {"image": 0, "relay": 0}  # image 0 = position_1, relay 0 = premier relais (8)

    # Bouton pour l'aiguillage 1
    button_aiguillage_1 = Button(
        root, image=img_position_1,
        command=lambda: bouton_clicked(button_aiguillage_1, relays[0], images, state_aiguillage_1),
        takefocus=True
    )
    button_aiguillage_1.pack(pady=10)

    # Légende pour l'aiguillage 1
    label_aiguillage_1 = Label(root, text="Aiguillage 1", font=("Arial", 14))
    label_aiguillage_1.pack(pady=5)

    # Bouton pour l'aiguillage 2
    button_aiguillage_2 = Button(
        root, image=img_position_1,
        command=lambda: bouton_clicked(button_aiguillage_2, relays[1], images, state_aiguillage_2),
        takefocus=True
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
        frame_slider, from_=-1, to=1, value=0, length=200, orient="horizontal",
        command=lambda val: update_vitesse(vitesse_slider, slider_value_label),  # Mise à jour du label
        takefocus=True
    )
    vitesse_slider.pack()
    
    # Affichage de la valeur du slider
    slider_value_label = Label(frame_slider, text="Vitesse: 0", font=("Arial", 14))
    slider_value_label.pack()

    # Attacher un événement pour simuler un clic sur les boutons avec Entrée
    button_aiguillage_1.bind('<Return>', lambda event: bouton_clicked(button_aiguillage_1, relays[0], images, state_aiguillage_1))  # Touche Entrée sur bouton1
    button_aiguillage_2.bind('<Return>', lambda event: bouton_clicked(button_aiguillage_2, relays[1], images, state_aiguillage_2))  # Touche Entrée sur bouton2

    # Fonction de gestion du focus sur slider avec "Enter"
    def handle_enter_on_slider(event):
        """Passe à la valeur suivante du cycle vitesse lorsque Enter est pressée."""
        current_cycle_index = (current_cycle_index + 1) % len(cycle_vitesse_states)
        new_value = cycle_vitesse_states[current_cycle_index]
        vitesse_slider.set(new_value)  # Met à jour la position du slider
        update_vitesse(vitesse_slider, slider_value_label)  # Réactualise l'affichage

    # Lier "Enter" au slider pour changer de valeur dans le cycle
    vitesse_slider.bind('<Return>', handle_enter_on_slider)

    # Variable globale pour garder l'état du cycle de la vitesse
    cycle_vitesse_states = [0, 1, 0, -1]
    current_cycle_index = 0

    def handle_enter_on_slider(event):
        """Passe à la valeur suivante du cycle vitesse lorsque Enter est pressée."""
        global current_cycle_index, cycle_vitesse_states
        # Passe au prochain état dans le cycle
        current_cycle_index = (current_cycle_index + 1) % len(cycle_vitesse_states)
        new_value = cycle_vitesse_states[current_cycle_index]
        vitesse_slider.set(new_value)  # Met à jour le slider
        update_vitesse(vitesse_slider, slider_value_label)  # Met à jour l'interface

    vitesse_slider.bind('<Return>', handle_enter_on_slider)

    # Initialisation de focus sur bouton1
    button_aiguillage_1.focus_set()

    # Démarrage de la boucle principale de l'interface
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
