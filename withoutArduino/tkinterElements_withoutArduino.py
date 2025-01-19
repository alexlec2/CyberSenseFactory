from ttkbootstrap import Scale, Menubutton, Meter, Button
from tkinter import IntVar
from tkinter import Label, Frame, Menu, Label
from PIL import Image, ImageTk  
Image.CUBIC = Image.BICUBIC
import json, random

import sys, os
from controlAiguillage_withoutArduino import activate_relay

speed_status = 0
current_cycle_index = 0
current_cycle_index_old = -1

def handle_enter_on_slider(vitesse_slider, slider_value_label, relays, current_cycle_index, current_cycle_index_old):
    """Passe à la valeur suivante du cycle vitesse lorsque Enter est pressée."""

    if current_cycle_index == 0 and current_cycle_index_old == -1:
        new_value = 1
    elif (current_cycle_index == 1 or current_cycle_index == -1)  and current_cycle_index_old == 0:
        new_value = 0
    elif current_cycle_index == 0 and current_cycle_index_old == 1:
        new_value = -1

    vitesse_slider.set(new_value)  # Met à jour le slider
    update_vitesse(vitesse_slider, slider_value_label, relays)  # Met à jour l'interface

def update_vitesse(slider, slider_value_label, relays, meters):
    """
    Mise à jour progressive du label de vitesse et des meters en fonction de la valeur du slider.
    Contrôle également l'état des relais.
    """
    global speed_status, current_cycle_index, current_cycle_index_old

    if current_cycle_index != current_cycle_index_old and int(slider.get()) != current_cycle_index:
        current_cycle_index_old = current_cycle_index
        current_cycle_index = int(slider.get())

    vitesse = int(slider.get()) * 10  # Obtient la valeur du slider
    slider_value_label.config(text=f"Vitesse: {vitesse}")

    # Variables pour la vitesse et la consommation des meters
    meter_vitesse = meters[2]
    meter_consommation = meters[0]

    # Valeurs cibles pour la vitesse et la consommation
    if vitesse == 10 and speed_status != 10:
        # board.digital[relays[2][1]].write(0)
        print(f"Activation du relais {relays[2][1]}.")
        # board.digital[relays[2][0]].write(1)
        print(f"Le relais {relays[2][0]} est à 0.")
        print("Le train avance")
        speed_status = 10
        target_vitesse = random.randint(250, 300)
        target_consommation = random.randint(800, 1000)

    elif vitesse == -10 and speed_status != -10:
        # board.digital[relays[2][0]].write(0)
        print(f"Activation du relais {relays[2][0]}.")
        # board.digital[relays[2][1]].write(1)
        print(f"Le relai {relays[2][1]} est à 0.")
        print("Le train recule")
        speed_status = -10
        target_vitesse = random.randint(250, 300)
        target_consommation = random.randint(800, 1000)

    elif vitesse == 0 and speed_status != 0:
        # board.digital[relays[2][1]].write(0)
        # board.digital[relays[2][0]].write(0)
        print(f"Le relais {relays[2][0]} est à 0.")
        print(f"Le relais {relays[2][1]} est à 0.")
        print("Le train est à l'arrêt")
        speed_status = 0
        target_vitesse = 0
        target_consommation = random.randint(100, 400)

    else:
        # Pas de changement de vitesse ou d'état
        return

    # Lancement des mises à jour progressives
    animate_meter_change(meter_vitesse, target_vitesse, step_duration=30)
    animate_meter_change(meter_consommation, target_consommation, step_duration=20)


def animate_meter_change(meter, target_value, step_duration):
    """
    Mise à jour progressive d'un meter vers une valeur cible en 1 seconde.
    :param meter: Meter à mettre à jour.
    :param target_value: Valeur cible à atteindre.
    """
    # Valeur actuelle du meter
    start_value = meter["amountused"]
    
    # Nombre d'étapes fixes et calcul du changement par étape
    step_count = 20
    step_size = (target_value - start_value) / step_count
    # step_duration = 33  # 1000ms / 30 steps ≈ 33ms par étape

    def update_step(current_step):
        # Calcul de la nouvelle valeur du meter pour l'étape actuelle
        new_value = start_value + step_size * current_step

        # Arrêter l'animation lorsque nous atteignons ou dépassons la valeur cible
        if current_step < step_count:
            meter.configure(amountused=int(new_value))
            meter.after(step_duration, update_step, current_step + 1)
        else:
            # Assurez-vous que la valeur cible est atteinte
            meter.configure(amountused=int(target_value))

    # Démarre l'animation
    update_step(0)



def bouton_clicked(board, button, relays, images, state, time_sleep):
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

def create_scada_frames(scada_frame, relays, margin, time_sleep):
    global current_cycle_index, current_cycle_index_old

    # Création de la première section (identique)
    section1 = Frame(scada_frame, bg="white", height=370, width=740)
    section1.grid(row=0, column=0, padx=margin, pady=margin)

    # Configuration de la grille pour les éléments dans section1
    section1.columnconfigure((0, 1, 2), weight=1)
    section1.rowconfigure(0, weight=9)
    section1.rowconfigure(1, weight=1)
    section1.rowconfigure(2, weight=1)

    # Étiquette de connexion (identique)
    status_label = Label(section1, text="Tentative de connexion à l'Arduino...", font=("Arial", 18), fg="blue")
    status_label.grid(row=0, column=0, columnspan=3, pady=25)
    
    # Initialisation des images et états (identique)
    max_height = 300
    img_position_1 = resize_image("images/position_1.png", max_height)
    img_position_2 = resize_image("images/position_2.png", max_height)
    img_position_3 = resize_image("images/position_3.png", max_height)
    img_position_4 = resize_image("images/position_4.png", max_height)

    images_list = [img_position_1, img_position_2]
    images_list2 = [img_position_3, img_position_4]

    state_aiguillage_1 = {"image": 0, "relay": 0}
    state_aiguillage_2 = {"image": 0, "relay": 0}

    # Boutons et légendes pour les aiguillages (identique)
    button_aiguillage_1 = Button(
        section1, image=img_position_1,
        command=lambda: bouton_clicked(scada_frame, button_aiguillage_1, relays[0], images_list, state_aiguillage_1, time_sleep),
        takefocus=True, bootstyle="success-link"
    )
    button_aiguillage_1.grid(row=1, column=0)
    label_aiguillage_1 = Label(section1, text="Aiguillage 1", font=("Arial", 14))
    label_aiguillage_1.grid(row=2, column=0)

    button_aiguillage_2 = Button(
        section1, image=img_position_3,
        command=lambda: bouton_clicked(scada_frame, button_aiguillage_2, relays[1], images_list2, state_aiguillage_2, time_sleep),
        takefocus=True, bootstyle="success-link"
    )
    button_aiguillage_2.grid(row=1, column=2)
    label_aiguillage_2 = Label(section1, text="Aiguillage 2", font=("Arial", 14))
    label_aiguillage_2.grid(row=2, column=2)

    # Slider vertical et label pour la vitesse
    frame_slider = section1
    vitesse_slider = Scale(
        frame_slider, from_=1, to=-1, value=0, length=200, orient="vertical",
        command=lambda val: update_vitesse(vitesse_slider, slider_value_label, relays, meters),  # Mise à jour dynamique
        takefocus=True
    )
    vitesse_slider.grid(row=1, column=1)

    slider_value_label = Label(frame_slider, text="Vitesse: 0", font=("Arial", 14), width=10)
    slider_value_label.grid(row=2, column=1, padx=20)

    # Attacher un événement pour simuler un clic sur les boutons avec Entrée
    button_aiguillage_1.bind('<Return>', lambda event: bouton_clicked(scada_frame, button_aiguillage_1, relays[0], images_list, state_aiguillage_1, time_sleep))  # Touche Entrée sur bouton1
    button_aiguillage_2.bind('<Return>', lambda event: bouton_clicked(scada_frame, button_aiguillage_2, relays[1], images_list2, state_aiguillage_2, time_sleep))  # Touche Entrée sur bouton2

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
        update_vitesse(vitesse_slider, slider_value_label, relays, meters)  # Met à jour l'interface

    vitesse_slider.bind('<Return>', handle_enter_on_slider)

    # Initialisation du focus
    button_aiguillage_1.focus_set()

    # Création de la deuxième section (modifiée pour inclure les plages)
    section2 = Frame(scada_frame, bg="white", height=300, width=740)
    section2.grid(row=1, column=0, padx=margin, pady=margin)

    section2.columnconfigure((0, 1, 2, 3), weight=1)
    section2.rowconfigure(0, weight=1)

    # Définition des meters
    meter_styles = ["warning", "info", "success"]
    meter_text = ["Consommation", "Capacité", "Vitesse"]
    meter_score_default = [100, random.randint(3000, 10000), 0]  # Valeurs initiales
    meter_max_value = [1000, 10000, 300]
    meter_text_right = ["kW/h", "/10000", "km/h"]
    meter_stripethickness = [10, 0, 2]

    meters = []  # Liste pour les meters, mise à jour avec le slider
    for i in range(3):
        meter = Meter(
            section2, metersize=275, amounttotal=meter_max_value[i], amountused=meter_score_default[i], 
            subtext=meter_text[i], subtextfont="-size 20", textright=meter_text_right[i],
            bootstyle=meter_styles[i], 
            metertype="semi",
            interactive=False,
            meterthickness=20,
            stripethickness=meter_stripethickness[i]
        )
        meter.grid(row=0, column=i, sticky="nsew", padx=15, pady=5)
        meters.append(meter)  # Ajout dans la liste

# Sauvegarde des relais dans le fichier
def save_relays(file_path, relays):
    with open(file_path, "w") as file:
        json.dump(relays, file)

def update_relays(index, new_value, relays, DB_PATH):
    """Met à jour la variable globale relays et enregistre les changements dans un fichier."""
    row, col = divmod(index, 2)
    relays[row][col] = new_value
    save_relays(DB_PATH, relays)  # Sauvegarder la nouvelle valeur dans le fichier
    print(f"Relays updated: {relays}")  # Debug : Affiche les relais mis à jour

def activer_relai(var):
    print(f"Relai {var.get()}")

def create_config_frame(config_frame, relays, DB_PATH, board):
    """
    Crée un tableau de configuration avec deux colonnes et trois lignes,
    chaque cellule contenant un Menubutton, son Label, et un bouton d'action stylisé associé.
    """
    # Définition des éléments et styles
    list_relays_elements = ["Aiguillage1 Relai n°1", "Aiguillage1 Relai n°2", "Aiguillage2 Relai n°1", "Aiguillage2 Relai n°2", "Train Relai n°1", "Train Relai n°2"]
    styles = ["primary", "primary", "info", "info", "danger", "danger"]
    default_values = [val for sublist in relays for val in sublist]

    # Configuration de la grille
    rows, cols = 3, 2  # 3 lignes et 2 colonnes
    for r in range(rows):
        config_frame.rowconfigure(r, weight=0)
    for c in range(cols):
        config_frame.columnconfigure(c, weight=1)

    for index, option in enumerate(list_relays_elements):
        row, col = divmod(index, 2)  # Calculer la ligne et la colonne à partir de l'index

        # Créer une frame pour regrouper les widgets
        widget_frame = Frame(config_frame)
        widget_frame.grid(row=row, column=col, padx=10, pady=50, sticky="n")

        # Ajouter le Menubutton dans la frame
        mb = Menubutton(widget_frame, text=option, bootstyle=styles[index])
        mb.pack()

        # Ajouter le Label juste en dessous dans la même frame
        label = Label(widget_frame, text=f"Relai séléctionné : {default_values[index]}", font=("Arial", 12))
        label.pack()

        # Ajouter un bouton d'action stylisé en dessous du Label
        action_button = Button(
            widget_frame,
            text=f"Test Relai {default_values[index]}",
            bootstyle=styles[index],
            command=lambda var=default_values[index]: print(f"Relai {var}"),
        )
        action_button.pack(pady=5)

        # Ajouter un menu déroulant pour changer la valeur
        menu = Menu(mb, tearoff=0)
        default_value = IntVar(value=default_values[index])

        def make_update_function(lbl, var, idx, btn):
            def update_label_and_button():
                # Met à jour le label
                lbl.config(text=f"Relai séléctionné : {var.get()}")
                # Met à jour le bouton
                btn.config(
                    text=f"Test Relai {var.get()}",
                    command=lambda: activer_relai(var),
                )
                # Met à jour la valeur du relai
                update_relays(idx, var.get(), relays, DB_PATH)

            return update_label_and_button

        # Options dans le menu déroulant
        for value in [13, 12, 8, 7, 4, 2]:
            menu.add_radiobutton(
                label=str(value),
                variable=default_value,
                value=value,
                command=make_update_function(label, default_value, index, action_button),
            )

        mb["menu"] = menu


# Fonction pour définir path data pyinstaller
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