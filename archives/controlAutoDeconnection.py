from base import connect_to_arduino, disconnect_from_arduino
from pynput import keyboard

# Initialisation
board = None
relay_pin = 13

# Connexion initiale
board = connect_to_arduino('UNO WiFi R4')
if not board:
    print("Impossible de se connecter à l'Arduino. Le programme va se fermer.")
    exit()

# Configurer la broche comme sortie
board.digital[relay_pin].mode = 1

def on_press(key):
    """Fonction appelée lors de la pression d'une touche."""
    global board
    try:
        if key.char == "s" and board:
            print("Relais activé (HIGH).")
            board.digital[relay_pin].write(1)
        elif key.char == "q":
            print("Programme terminé.\n")
            return False
    except AttributeError:
        pass

def on_release(key):
    """Fonction appelée lors du relâchement d'une touche."""
    global board
    try:
        if key.char == "s" and board:
            print("Relais désactivé (LOW).")
            board.digital[relay_pin].write(0)
            disconnect_from_arduino(board)
            board = None  # Indiquer que l'Arduino est déconnecté

            # Reconnexion automatique
            print("Tentative de reconnexion à l'Arduino...")
            board = connect_to_arduino()
            if board:
                board.digital[relay_pin].mode = 1  # Configurer la broche comme sortie
            else:
                print("La reconnexion a échoué.")
    except AttributeError:
        pass

print("Maintenez la touche 'S' pour activer le relais.")
print("Relâchez la touche 'S' pour désactiver le relais et reconnecter l'Arduino.")
print("Appuyez sur 'Q' pour quitter le programme.\n")

# Écoute des touches
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Déconnexion finale si le programme est quitté
disconnect_from_arduino(board)
