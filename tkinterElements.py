from ttkbootstrap import Scale, Menubutton, Meter, Button
from tkinter import IntVar
from tkinter import Label, Frame, Menu, Label
from PIL import Image, ImageTk  
Image.CUBIC = Image.BICUBIC
import random, time

import sys, os

speed_status = 0
current_cycle_index = 0
current_cycle_index_old = -1

def activate_relay(board, relay_pin, time_sleep):
    if relay_pin == 4 or relay_pin == 2:
        board.digital[relay_pin].write(0)
        time.sleep(time_sleep)
        board.digital[relay_pin].write(1)
    else:
        board.digital[relay_pin].write(1)
        time.sleep(time_sleep)
        board.digital[relay_pin].write(0)

def handle_enter_on_slider(board, vitesse_slider, slider_value_label, relays, current_cycle_index, current_cycle_index_old):
    """Passe à la valeur suivante du cycle vitesse lorsque Enter est pressée."""

    if current_cycle_index == 0 and current_cycle_index_old == -1:
        new_value = 1
    elif (current_cycle_index == 1 or current_cycle_index == -1)  and current_cycle_index_old == 0:
        new_value = 0
    elif current_cycle_index == 0 and current_cycle_index_old == 1:
        new_value = -1

    vitesse_slider.set(new_value)
    update_vitesse(board, vitesse_slider, slider_value_label, relays)

def update_vitesse(board, slider, slider_value_label, relays, meters):
    """
    Mise à jour progressive du label de vitesse et des meters en fonction de la valeur du slider.
    Contrôle également l'état des relais.
    """
    global speed_status, current_cycle_index, current_cycle_index_old

    if current_cycle_index != current_cycle_index_old and int(slider.get()) != current_cycle_index:
        current_cycle_index_old = current_cycle_index
        current_cycle_index = int(slider.get())

    vitesse = int(slider.get()) * 10 
    slider_value_label.config(text=f"Vitesse: {vitesse}")

    meter_vitesse = meters[2]
    meter_consommation = meters[0]

    if vitesse == 10 and speed_status != 10:
        board.digital[relays[2][1]].write(0)
        board.digital[relays[2][0]].write(1)
        speed_status = 10
        target_vitesse = random.randint(250, 300)
        target_consommation = random.randint(800, 1000)

    elif vitesse == -10 and speed_status != -10:
        board.digital[relays[2][0]].write(0)
        board.digital[relays[2][1]].write(1)
        speed_status = -10
        target_vitesse = random.randint(250, 300)
        target_consommation = random.randint(800, 1000)

    elif vitesse == 0 and speed_status != 0:
        board.digital[relays[2][1]].write(0)
        board.digital[relays[2][0]].write(0)
        speed_status = 0
        target_vitesse = 0
        target_consommation = random.randint(100, 400)

    else:
        return

    animate_meter_change(meter_vitesse, target_vitesse, slider, step_duration=30)
    animate_meter_change(meter_consommation, target_consommation, slider, step_duration=20)


def animate_meter_change(meter, target_value, slider, step_duration):
    start_value = meter["amountused"]

    step_count = 15
    step_size = (target_value - start_value) / step_count

    def update_step(current_step):
        new_value = start_value + step_size * current_step

        if current_step < step_count:
            meter.configure(amountused=int(new_value))
            meter.after(step_duration, update_step, current_step + 1)
        else:
            meter.configure(amountused=int(target_value))

    update_step(0)





def bouton_clicked(board, button, relays, images, state, time_sleep):
    new_state = 1 - state["image"]
    button.config(image=images[new_state])
    state["image"] = new_state
    relay_to_activate = relays[state["relay"]]
    activate_relay(board, relay_to_activate, time_sleep)
    state["relay"] = 1 - state["relay"]

def create_scada_frames(board, scada_frame, relays, margin, time_sleep):
    global current_cycle_index, current_cycle_index_old

    section1 = Frame(scada_frame, bg="white", height=320, width=780)
    section1.grid(row=0, column=0, padx=margin, pady=margin)

    section1.columnconfigure((0, 1, 2), weight=1)
    section1.rowconfigure(0, weight=9)
    section1.rowconfigure(1, weight=1)
    section1.rowconfigure(2, weight=1)

    status_label = Label(section1, text="Tentative de connexion à l'Arduino...", font=("Arial", 18), fg="blue")
    status_label.grid(row=0, column=0, columnspan=3, pady=25)
    
    img_position_1 = ImageTk.PhotoImage(Image.open(resource_path("images/position_1.png")))
    img_position_2 = ImageTk.PhotoImage(Image.open(resource_path("images/position_2.png")))
    img_position_3 = ImageTk.PhotoImage(Image.open(resource_path("images/position_3.png")))
    img_position_4 = ImageTk.PhotoImage(Image.open(resource_path("images/position_4.png")))


    images_list = [img_position_1, img_position_2]
    images_list2 = [img_position_3, img_position_4]

    state_aiguillage_1 = {"image": 0, "relay": 0}
    state_aiguillage_2 = {"image": 0, "relay": 0}

    button_aiguillage_1 = Button(
        section1, image=img_position_1,
        command=lambda: bouton_clicked(board, button_aiguillage_1, relays[0], images_list, state_aiguillage_1, time_sleep),
        takefocus=True, state="normal", bootstyle="success-link"
    )
    button_aiguillage_1.grid(row=1, column=0)
    label_aiguillage_1 = Label(section1, text="Aiguillage 1", font=("Arial", 14))
    label_aiguillage_1.grid(row=2, column=0)

    button_aiguillage_2 = Button(
        section1, image=img_position_3,
        command=lambda: bouton_clicked(board, button_aiguillage_2, relays[1], images_list2, state_aiguillage_2, time_sleep),
        takefocus=True, state="normal", bootstyle="success-link"
    )
    button_aiguillage_2.grid(row=1, column=2)
    label_aiguillage_2 = Label(section1, text="Aiguillage 2", font=("Arial", 14))
    label_aiguillage_2.grid(row=2, column=2)

    frame_slider = section1
    vitesse_slider = Scale(
        frame_slider, from_=1, to=-1, value=0, length=200, orient="vertical",
        command=lambda val: update_vitesse(board, vitesse_slider, slider_value_label, relays, meters),  # Mise à jour dynamique
        takefocus=True, state="normal"
    )
    vitesse_slider.grid(row=1, column=1)

    slider_value_label = Label(frame_slider, text="Vitesse: 0", font=("Arial", 14), width=10)
    slider_value_label.grid(row=2, column=1, padx=20)

    button_aiguillage_1.bind('<Return>', lambda event: bouton_clicked(board, button_aiguillage_1, relays[0], images_list, state_aiguillage_1, time_sleep))  # Touche Entrée sur bouton1
    button_aiguillage_2.bind('<Return>', lambda event: bouton_clicked(board, button_aiguillage_2, relays[1], images_list2, state_aiguillage_2, time_sleep))  # Touche Entrée sur bouton2

    vitesse_slider.bind('<Return>', lambda val: handle_enter_on_slider(board, vitesse_slider, slider_value_label, relays, current_cycle_index, current_cycle_index_old))

    button_aiguillage_1.focus_set()

    section2 = Frame(scada_frame, bg="white", height=260, width=780)
    section2.grid(row=1, column=0, padx=margin, pady=margin)

    section2.columnconfigure((0, 1, 2, 3), weight=1)
    section2.rowconfigure(0, weight=1)

    meter_styles = ["warning", "info", "success"]
    meter_text = ["Consommation", "Capacité", "Vitesse"]
    meter_score_default = [100, random.randint(3000, 10000), 0]
    meter_max_value = [1000, 10000, 300]
    meter_text_right = ["kW/h", "/10000", "km/h"]
    meter_stripethickness = [10, 0, 2]

    meters = []
    for i in range(3):
        meter = Meter(
            section2, metersize=200, amounttotal=meter_max_value[i], amountused=meter_score_default[i], 
            subtext=meter_text[i], subtextfont="-size 10", textright=meter_text_right[i],
            bootstyle=meter_styles[i], 
            metertype="semi",
            interactive=False,
            meterthickness=20,
            stripethickness=meter_stripethickness[i]
        )
        meter.grid(row=0, column=i, sticky="nsew", padx=15, pady=5)
        meters.append(meter)
    
    ui_elements = [button_aiguillage_1, button_aiguillage_2, vitesse_slider]
    return ui_elements, status_label


def update_relays(index, new_value, relays):
    """Met à jour la variable globale relays et enregistre les changements dans un fichier."""
    row, col = divmod(index, 2)
    relays[row][col] = new_value

def activer_relai(board, var):
    if var == 4 or var == 2:
        board.digital[var].write(0)
        time.sleep(1)
        board.digital[var].write(1)
    else:
        board.digital[var].write(1)
        time.sleep(1)
        board.digital[var].write(0)

def create_config_frame(config_frame, relays, board):

    list_relays_elements = ["Aiguillage1 Relai n°1", "Aiguillage1 Relai n°2", "Aiguillage2 Relai n°1", "Aiguillage2 Relai n°2", "Train Relai n°1", "Train Relai n°2"]
    styles = ["primary", "primary", "info", "info", "danger", "danger"]
    default_values = [val for sublist in relays for val in sublist]

    rows, cols = 3, 2 
    for r in range(rows):
        config_frame.rowconfigure(r, weight=0)
    for c in range(cols):
        config_frame.columnconfigure(c, weight=1)

    for index, option in enumerate(list_relays_elements):
        row, col = divmod(index, 2) 

        widget_frame = Frame(config_frame)
        widget_frame.grid(row=row, column=col, padx=10, pady=50, sticky="n")

        mb = Menubutton(widget_frame, text=option, bootstyle=styles[index])
        mb.pack()

        label = Label(widget_frame, text=f"Relai séléctionné : {default_values[index]}", font=("Arial", 12))
        label.pack()

        action_button = Button(
            widget_frame,
            text=f"Test Relai {default_values[index]}",
            bootstyle=styles[index],
            command=lambda var=default_values[index]: activer_relai(board, var),
        )
        action_button.pack(pady=5)

        menu = Menu(mb, tearoff=0)
        default_value = IntVar(value=default_values[index])

        def make_update_function(lbl, var, idx, btn):
            def update_label_and_button():
                lbl.config(text=f"Relai séléctionné : {var.get()}")
                btn.config(
                    text=f"Test Relai {var.get()}",
                    command=lambda: activer_relai(board, var.get()),
                )
                update_relays(idx, var.get(), relays)

            return update_label_and_button

        for value in [13, 12, 8, 7, 4, 2]:
            menu.add_radiobutton(
                label=str(value),
                variable=default_value,
                value=value,
                command=make_update_function(label, default_value, index, action_button),
            )

        mb["menu"] = menu


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)