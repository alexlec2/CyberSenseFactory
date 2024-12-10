from pyfirmata2 import Arduino, util
import serial.tools.list_ports
from pynput import keyboard
import time


def find_arduino():
    """Detecte automatiquement le port de l'Arduino et retourne son nom de port."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "UNO WiFi R4" in port.description or "tty" in port.device or "COM" in port.device:
            return port
    raise IOError("Aucun Arduino detecte. Verifiez la connexion.")

# Trouver et attribue automatiquement le port de l'Arduino
try:
    port = find_arduino()
    print(f"Arduino detecte sur le port : {port.device}\n")
    print(f"Connexion en cours avec l'Arduino {port.description}\n")
    board = Arduino(port.device)
    print(f"Connecte avec succes avec l'Arduino {port.description}\n")
except IOError as e:
    print(e)
    exit()


# Definir la broche du relais
relay_1 = 13
relay_2 = 12
board.digital[relay_1].mode = 1  # Configurer la broche comme sortie OUTPUT
board.digital[relay_2].mode = 1  # Configurer la broche comme sortie OUTPUT

print("Appuyez sur 'H' pour activer le relais et sur 'L' pour le desactiver.")
print("Appuyez sur 'Q' pour quitter le programme.\n")

board.digital[relay_1].write(1)
board.digital[relay_2].write(0)

def on_press(key):
    """Fonction appelee lors de la pression d'une touche."""
    try:
        if key.char == "h":  # Activer le relais avec la touche 'H'
            print(board)
            print("Relais active (HIGH).")
            board.digital[relay_1].write(1)
            # time.sleep(0.05) 
            board.digital[relay_2].write(0)
            # time.sleep(3)  # Pause de 3 secondes
        elif key.char == "l":  # Desactiver le relais avec la touche 'L'
            print(board)
            print("Relais desactive (LOW).")
            board.digital[relay_1].write(0)
            # time.sleep(0.05)
            board.digital[relay_2].write(1)
            # time.sleep(3)  # Pause de 3 secondes
        # elif key.char == "q":  # Activer le relais avec la touche 'H'
        #     print("Relais active (HIGH).")
        #     board.digital[relay_2].write(1)
        # elif key.char == "d":  # Desactiver le relais avec la touche 'L'
        #     print("Relais desactive (LOW).")
        #     board.digital[relay_2].write(0)
        elif key.char == "q":  # Quitter avec la touche 'Q'
            print("Programme termine.\n")
            return False
    except AttributeError:
        pass  # Ignore les touches speciales comme Shift ou Ctrl


# ecoute des touches
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# Arreter proprement la connexion a l'Arduino
board.exit()
