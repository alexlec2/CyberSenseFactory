from base import connect_to_arduino, disconnect_from_arduino, init_relay_output
from controlAiguillage import activate_relay
from pynput import keyboard


def on_press(key):
    """Fonction appelée lors de la pression d'une touche."""
    global last_activated_relay_1
    global last_activated_relay_2

    try:
        if key.char == "a":  # Active le relais 13
            activate_relay(board, relays[0][0], last_activated_relay_1)
            last_activated_relay_1 = relays[0][0]
        elif key.char == "z":  # Active le relais 12
            activate_relay(board, relays[0][1], last_activated_relay_1)
            last_activated_relay_1 = relays[0][1]
        elif key.char == "o":  # Active le relais 12
            activate_relay(board, relays[1][0], last_activated_relay_2)
            last_activated_relay_2 = relays[1][0]
        elif key.char == "p":  # Active le relais 12
            activate_relay(board, relays[1][1], last_activated_relay_2)
            last_activated_relay_2 = relays[1][1]
        elif key.char == "q":  # Quitter avec 'Q'
            print("Programme terminé.\n")
            return False
    except AttributeError:
        pass

# Initialisation
board = None
relays = [[13, 12], [8, 7]] # Duo de d'input pour les relays
last_activated_relay_1 = relays[0][0]  # Variable pour suivre le dernier relais activé entre le 13 et le 12
last_activated_relay_2 = relays[1][0]  # Variable pour suivre le dernier relais activé entre le 8 et le 7

# Connexion initiale avec le Arduino en fonction de son nom
name_arduino = "UNO WiFi R4"

board = connect_to_arduino(name_arduino)
if not board:
    print("Impossible de se connecter à l'Arduino. Le programme va se fermer.")
    exit()

# Initialise les relais en OUTPUT et en state LOW
init_relay_output(board, relays)

print("Appuyez sur 'A' pour activer le relais 13 pendant 0,25 seconde (si ce n'était pas le dernier activé).")
print("Appuyez sur 'Z' pour activer le relais 12 pendant 0,25 seconde (si ce n'était pas le dernier activé).")
print("Appuyez sur 'O' pour activer le relais 8 pendant 0,25 seconde (si ce n'était pas le dernier activé).")
print("Appuyez sur 'P' pour activer le relais 7 pendant 0,25 seconde (si ce n'était pas le dernier activé).")
print("Appuyez sur 'Q' pour quitter le programme.\n")

# Écoute des touches et call la fonction on press
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# Déconnexion finale
disconnect_from_arduino(board)
print("Déconnexion de l'Arduino.")

# Control 2 aiguillages connected with a remote controller and two relays each one.
# Code that activate during 0.25 second relay if it was not the last relay activated.

# Precisely :
# - when you press 'A' and last relay HIGH is not 13, it will activate relay 13 during 0.25 seconds.
# - when you press 'Z' and last relay HIGH is not 12, it will activate relay 12 during 0.25 seconds.
# - when you press 'O' and last relay HIGH is not 8, it will activate relay 8 during 0.25 seconds.
# - when you press 'P' and last relay HIGH is not 7, it will activate relay 7 during 0.25 seconds.