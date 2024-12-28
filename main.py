from base import connect_to_arduino, disconnect_from_arduino, init_relay_output
from controlAiguillage import activate_relay
from pynput import keyboard


def on_press(key):
    """Fonction appelée lors de la pression d'une touche."""

    try:
        if key.char == "a":  # Active le relais 13
            activate_relay(board, relays[0][0], time_sleep)
        elif key.char == "z":  # Active le relais 12
            activate_relay(board, relays[0][1], time_sleep)
        elif key.char == "o":  # Active le relais 8
            activate_relay(board, relays[1][0], time_sleep)
        elif key.char == "p":  # Active le relais 7
            activate_relay(board, relays[1][1], time_sleep)
        elif key.char == "q":  # Quitter avec 'Q'
            print("Programme terminé.\n")
            return False
    except AttributeError:
        pass

# Initialisation
board = None
time_sleep = 0.5 # Time that relay will be activated, value in second 
relays = [[13, 12], [8, 7]] # Duo de d'input pour les relays

# Connexion initiale avec le Arduino en fonction de son nom
name_arduino = "UNO WiFi R4"

board = connect_to_arduino(name_arduino)
if not board:
    print("Impossible de se connecter à l'Arduino. Le programme va se fermer.")
    exit()

# Initialise les relais en OUTPUT et en state LOW
init_relay_output(board, relays)

print("Appuyez sur 'A' pour activer le relais 13 pendant 0,5 seconde.")
print("Appuyez sur 'Z' pour activer le relais 12 pendant 0,5 seconde.")
print("Appuyez sur 'O' pour activer le relais 8 pendant 0,5 seconde.")
print("Appuyez sur 'P' pour activer le relais 7 pendant 0,5 seconde.")
print("Appuyez sur 'Q' pour quitter le programme.\n")

# Écoute des touches et call la fonction on press
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# Déconnexion finale
disconnect_from_arduino(board)
print("Déconnexion de l'Arduino.")

# Control 2 aiguillages connected with a remote controller and two relays each one.
# Code that activate during 0.5 second the asociated relay.
