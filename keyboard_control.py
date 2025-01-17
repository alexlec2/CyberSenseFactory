from base import connect_to_arduino, disconnect_from_arduino, init_relay_output
from controlAiguillage import activate_relay
from pynput import keyboard
from threading import Timer

# Temps d'inactivité avant de désactiver les relais (en secondes)
INACTIVITY_TIMEOUT = 0.5

# Variable pour garder trace du temporisateur actif
inactivity_timer = None

def reset_relays():
    """Réinitialise les relais lorsque aucune touche n'est pressée."""
    print("Aucune touche n'a été pressée. Réinitialisation des relais...")
    print("Le train est à l'arrêt.")
    board.digital[relays[2][0]].write(0)
    board.digital[relays[2][1]].write(0)

def on_press(key):
    """Fonction appelée lors de la pression d'une touche."""

    global inactivity_timer  # Accède au temporisateur global

    # Si une touche est pressée, annule le précédent timer (s'il existe) et démarre un nouveau timer
    if inactivity_timer is not None:
        inactivity_timer.cancel()

    try:
        if key.char == "a":  # Active le relais 13
            activate_relay(board, relays[0][0], time_sleep)
        elif key.char == "z":  # Active le relais 12
            activate_relay(board, relays[0][1], time_sleep)
        elif key.char == "o":  # Active le relais 8
            activate_relay(board, relays[1][0], time_sleep)
        elif key.char == "p":  # Active le relais 7
            activate_relay(board, relays[1][1], time_sleep)
        elif key.char == "w":  # Active le relais 4
            board.digital[relays[2][0]].write(0)
            board.digital[relays[2][1]].write(1)
            print("Le train recule.")
        elif key.char == "x":  # Active le relais 2
            board.digital[relays[2][1]].write(0)
            board.digital[relays[2][0]].write(1)
            print("Le train avance.")
        elif key.char == "q":  # Quitter avec 'Q'
            print("Programme terminé.\n")
            return False
    except AttributeError:
        pass

    # Relance le timer d'inactivité à chaque pression de touche
    inactivity_timer = Timer(INACTIVITY_TIMEOUT, reset_relays)
    inactivity_timer.start()

# Initialisation
board = None
time_sleep = 0.5 # Time that relay will be activated, value in second 
relays = [[13, 12], [8, 7], [4, 2]] # Trio de d'input pour les relays

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
print("Appuyez sur 'X' pour activer le relais 4 et faire avancer le train.")
print("Appuyez sur 'W' pour activer le relais 2 et faire reculer le train.")
print("Appuyez sur 'Q' pour quitter le programme.\n")

# Écoute des touches et call la fonction on press
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# Déconnexion finale
disconnect_from_arduino(board)
print("Déconnexion de l'Arduino.")

# Control 2 aiguillages connected with a remote controller and two relays each one.
# Code that activate during 0.5 second the asociated relay.
