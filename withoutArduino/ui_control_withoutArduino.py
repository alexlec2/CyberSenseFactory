from tkinter import Tk, Button, Label, Frame
from PIL import Image, ImageTk  # Importation pour redimensionner les images
Image.CUBIC = Image.BICUBIC
from controlAiguillage_withoutArduino import activate_relay
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sys
import os

# Initialisation
board = None
time_sleep = 0.5  # Durée d'activation du relais (en secondes)
relays = [[13, 12], [8, 7], [4, 2]]  # Duo d'input pour les relais
speed_status = 0
current_cycle_index = 0
current_cycle_index_old = -1

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Fonction de redimensionnement des images
def resize_image(file_path, max_height):
    """
    Redimensionne une image tout en gardant ses proportions pour une hauteur maximale.
    Ajoute une option pour retourner l'image en miroir.
    
    Args:
        file_path (str): Chemin du fichier image.
        max_height (int): Hauteur maximale souhaitée.
        mirror (bool): Si True, retourne l'image horizontalement.

    Returns:
        ImageTk.PhotoImage: Image redimensionnée et (éventuellement) retournée.
    """
    image = Image.open(resource_path(file_path))

    width, height = image.size

    # Redimensionnement si nécessaire
    if height > max_height:
        new_width = int(max_height * width / height)
        image = image.resize((new_width+40, max_height), Image.Resampling.LANCZOS)

    return ImageTk.PhotoImage(image)

# Affichage de la vitesse sélectionnée avec un slider
def update_vitesse(slider, slider_value_label):
    """Mise à jour du label de vitesse en fonction de la valeur du slider + activate relay of vitesse"""
    global speed_status, current_cycle_index, current_cycle_index_old

    if current_cycle_index != current_cycle_index_old and int(slider.get()) != current_cycle_index:
        current_cycle_index_old = current_cycle_index
        current_cycle_index = int(slider.get())

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
    print(images)
    new_state = 1 - state["image"]
    button.config(image=images[new_state])  # Met à jour l'image sur le bouton
    state["image"] = new_state

    # Active le relais correspondant
    relay_to_activate = relays[state["relay"]]
    activate_relay(board, relay_to_activate, time_sleep)
    print(f"Relais activé : {relay_to_activate}")

    # Alterne entre les deux relais
    state["relay"] = 1 - state["relay"]

def create_element_with_label(parent, element, element_args, text, row, column):
    # Créer l'élément
    widget = element(parent, **element_args)
    widget.grid(row=row, column=column)

    # Créer le label associé
    label = Label(parent, text=text, bg="white")
    label.grid(row=row + 1, column=column)

    return widget, label

def create_frames(root, margin):
    # Création de la première section
    section1 = Frame(root, bg="white", height=370, width=740)
    section1.grid(row=0, column=0, padx=margin, pady=margin)

    # Configuration de la grille pour les éléments dans section1
    section1.columnconfigure((0, 1, 2), weight=1)  # 3 colonnes pour les éléments
    section1.rowconfigure(0, weight=9)  # Ligne pour les éléments
    section1.rowconfigure(1, weight=1)  # Ligne pour les labels
    section1.rowconfigure(2, weight=1)  # Ligne pour les labels

    # Étiquette de connexion
    status_label = Label(section1, text="Tentative de connexion à l'Arduino...", font=("Arial", 18), fg="blue")
    status_label.grid(row=0, column=0, columnspan=3, pady=25)
    
    # Obtenez la hauteur dynamique de la section 1
    max_height = 300
    img_position_1 = resize_image("images/position_1.png", max_height)
    img_position_2 = resize_image("images/position_2.png", max_height)
    img_position_3 = resize_image("images/position_3.png", max_height)
    img_position_4 = resize_image("images/position_4.png", max_height)

    images_list = [img_position_1, img_position_2]
    images_list2 = [img_position_3, img_position_4]

    # États initiaux des aiguillages
    state_aiguillage_1 = {"image": 0, "relay": 0}
    state_aiguillage_2 = {"image": 0, "relay": 0}

    # Bouton et légende pour l'aiguillage 1
    button_aiguillage_1 = Button(
        section1, image=img_position_1,
        command=lambda: bouton_clicked(button_aiguillage_1, relays[0], images_list, state_aiguillage_1),
        takefocus=True
    )
    button_aiguillage_1.grid(row=1, column=0)
    label_aiguillage_1 = Label(section1, text="Aiguillage 1", font=("Arial", 14))
    label_aiguillage_1.grid(row=2, column=0)

    # Bouton et légende pour l'aiguillage 2
    button_aiguillage_2 = Button(
        section1, image=img_position_3,
        command=lambda: bouton_clicked(button_aiguillage_2, relays[1], images_list2, state_aiguillage_2),
        takefocus=True
    )
    button_aiguillage_2.grid(row=1, column=2)
    label_aiguillage_2 = Label(section1, text="Aiguillage 2", font=("Arial", 14))
    label_aiguillage_2.grid(row=2, column=2)

    # Slider vertical
    frame_slider = section1
    vitesse_slider = ttk.Scale(
        frame_slider, from_=1, to=-1, value=0, length=200, orient="vertical",
        command=lambda val: update_vitesse(vitesse_slider, slider_value_label),  # Mise à jour du label
        takefocus=True
    )
    vitesse_slider.grid(row=1, column=1)

    # Affichage de la valeur du slider
    slider_value_label = Label(frame_slider, text="Vitesse: 0", font=("Arial", 14), width=10)
    slider_value_label.grid(row=2, column=1, padx=40)

    # Attacher un événement pour simuler un clic sur les boutons avec Entrée
    button_aiguillage_1.bind('<Return>', lambda event: bouton_clicked(button_aiguillage_1, relays[0], images_list, state_aiguillage_1))  # Touche Entrée sur bouton1
    button_aiguillage_2.bind('<Return>', lambda event: bouton_clicked(button_aiguillage_2, relays[1], images_list2, state_aiguillage_2))  # Touche Entrée sur bouton2

    def handle_enter_on_slider(event):
        """Passe à la valeur suivante du cycle vitesse lorsque Enter est pressée."""
        global current_cycle_index, cycle_vitesse_states, current_cycle_index_old
        # Passe au prochain état dans le cycle

        if current_cycle_index == 0 and current_cycle_index_old == -1:
            new_value = 1
        elif (current_cycle_index == 1 or current_cycle_index == -1)  and current_cycle_index_old == 0:
            new_value = 0
        elif current_cycle_index == 0 and current_cycle_index_old == 1:
            new_value = -1

        vitesse_slider.set(new_value)  # Met à jour le slider
        update_vitesse(vitesse_slider, slider_value_label)  # Met à jour l'interface

    vitesse_slider.bind('<Return>', handle_enter_on_slider)

    # Initialisation de focus sur bouton1
    button_aiguillage_1.focus_set()

    # Création de la deuxième section
    section2 = Frame(root, bg="white", height=300, width=740)
    section2.grid(row=1, column=0, padx=margin, pady=margin)

    # Configuration pour afficher 4 meters alignés horizontalement
    section2.columnconfigure((0, 1, 2, 3), weight=1)
    section2.rowconfigure(0, weight=1)


    meter_styles = ["success", "info", "danger"]
    meter_text = ["Batterie", "Indice météo", "Température"]
    meter_score_default = [79, 34, 55]
    meter_text_right = ["%", "/100", "°C"]

    for i in range(3):
        meter = ttk.Meter(
            section2, metersize=275, amounttotal=100, amountused=meter_score_default[i], 
            subtext=meter_text[i], subtextfont="-size 20", textright=meter_text_right[i],
            bootstyle=meter_styles[i], 
            interactive=True
        )
        meter.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)

# Création de l'interface utilisateur
def create_ui():
    # global vitesse_slider  # Rendre la variable disponible dans la fonction d'événement
    # global slider_value_label, current_cycle_index, cycle_vitesse_states

    # root = Tk()
    # root.title("Contrôle Aiguillages")
    # root.geometry("1000x500")  # Taille adaptée pour les boutons et légendes

    # # Chargement et redimensionnement des images
    # max_height = 300
    # img_position_1 = resize_image("images/position_1.png", max_height)
    # img_position_2 = resize_image("images/position_2.png", max_height)
    # img_position_3 = resize_image("images/position_3.png", max_height)
    # img_position_4 = resize_image("images/position_4.png", max_height)

    # images_list = [img_position_1, img_position_2]
    # images_list2 = [img_position_3, img_position_4]

    # # États initiaux des aiguillages
    # state_aiguillage_1 = {"image": 0, "relay": 0}  # image 0 = position_1, relay 0 = premier relais (13)
    # state_aiguillage_2 = {"image": 0, "relay": 0}  # image 0 = position_1, relay 0 = premier relais (8)

    # # Bouton pour l'aiguillage 1
    # button_aiguillage_1 = Button(
    #     root, image=img_position_1,
    #     command=lambda: bouton_clicked(button_aiguillage_1, relays[0], images_list, state_aiguillage_1),
    #     takefocus=True
    # )
    # button_aiguillage_1.place(x=100, y=100)

    # # Bouton pour l'aiguillage 2
    # button_aiguillage_2 = Button(
    #     root, image=img_position_3,
    #     command=lambda: bouton_clicked(button_aiguillage_2, relays[1], images_list2, state_aiguillage_2),
    #     takefocus=True
    # )
    # button_aiguillage_2.place(x=600, y=100)


    # # Légende pour l'aiguillage 1
    # label_aiguillage_1 = Label(root, text="Aiguillage 1", font=("Arial", 14))
    # label_aiguillage_1.place(x=150, y=210)

    # # Légende pour l'aiguillage 2
    # label_aiguillage_2 = Label(root, text="Aiguillage 2", font=("Arial", 14))
    # label_aiguillage_2.place(x=600, y=210)

    # # Création du slider de vitesse
    # frame_slider = ttk.Frame(root)
    # frame_slider.place(x=300, y=200)

    # # Slider avec plage de -100% à +100%
    # vitesse_slider = ttk.Scale(
    #     frame_slider, from_=-1, to=1, value=0, length=200, orient="vertical",
    #     command=lambda val: update_vitesse(vitesse_slider, slider_value_label),  # Mise à jour du label
    #     takefocus=True
    # )
    # vitesse_slider.pack()
    
    # # Affichage de la valeur du slider
    # slider_value_label = Label(frame_slider, text="Vitesse: 0", font=("Arial", 14))
    # slider_value_label.pack()

    # # Attacher un événement pour simuler un clic sur les boutons avec Entrée
    # button_aiguillage_1.bind('<Return>', lambda event: bouton_clicked(button_aiguillage_1, relays[0], images_list, state_aiguillage_1))  # Touche Entrée sur bouton1
    # button_aiguillage_2.bind('<Return>', lambda event: bouton_clicked(button_aiguillage_2, relays[1], images_list2, state_aiguillage_2))  # Touche Entrée sur bouton2

    # def handle_enter_on_slider(event):
    #     """Passe à la valeur suivante du cycle vitesse lorsque Enter est pressée."""
    #     global current_cycle_index, cycle_vitesse_states, current_cycle_index_old
    #     # Passe au prochain état dans le cycle

    #     if current_cycle_index == 0 and current_cycle_index_old == -1:
    #         new_value = 1
    #     elif (current_cycle_index == 1 or current_cycle_index == -1)  and current_cycle_index_old == 0:
    #         new_value = 0
    #     elif current_cycle_index == 0 and current_cycle_index_old == 1:
    #         new_value = -1

    #     vitesse_slider.set(new_value)  # Met à jour le slider
    #     update_vitesse(vitesse_slider, slider_value_label)  # Met à jour l'interface

    # vitesse_slider.bind('<Return>', handle_enter_on_slider)

    # # Initialisation de focus sur bouton1
    # button_aiguillage_1.focus_set()
    # Configuration de la fenêtre principale
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

    # Appel de la fonction pour créer les frames
    create_frames(root, margin)

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
