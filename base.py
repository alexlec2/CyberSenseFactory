from pyfirmata2 import Arduino, util
import serial.tools.list_ports

# def find_arduino(name):
#     """Détecte automatiquement le port de l'Arduino et retourne son nom de port."""
#     ports = serial.tools.list_ports.comports()
#     for port in ports:
#         if name in port.description or "tty" in port.device or "COM" in port.device:
#             return port
#     raise IOError("Aucun Arduino détecté. Vérifiez la connexion.")

def connect_to_arduino(name):
    """Établit la connexion à l'Arduino."""
    try:
        # port = find_arduino(name)
        port = Arduino.AUTODETECT
        print(f"Connexion en cours avec l'Arduino sur le port {port}...")
        board = Arduino(port)
        print(f"Connecté avec succès à l'Arduino {port}.\n")
        return board
    except IOError as e:
        print(e)
        return None

def disconnect_from_arduino(board):
    """Ferme proprement la connexion à l'Arduino."""
    if board:
        print("Déconnexion de l'Arduino...")
        board.exit()
        print("Arduino déconnecté.\n")


def init_relay_output(board, relays):
    """Initialise les relays du arduino"""
    # Configurer les broches comme sorties
    for relay in relays:
        for output in relay:
            board.digital[output].mode = 1
            board.digital[output].write(0)
