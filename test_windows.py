import pyfirmata2
import serial.tools.list_ports

def find_arduino():
    """Recherche les ports série disponibles et retourne le bon port Arduino si trouvé."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"{port}")
        print(f"Port détecté : {port.device} (Description : {port.description})")  # Affichage du port
        # Vérification de l'élément de la description pour la présence de "Arduino" ou d'autres indications
        if "Arduino" in port.device or "usb" in port.device.lower():
            return port.device  # Retourner le port trouvé
    return None  # Aucun Arduino trouvé

def connect_to_arduino():
    """Établit la connexion à l'Arduino via un port série."""
    try:
        port = find_arduino()  # Recherche du port
        if port is None:
            print("Aucun Arduino connecté, aucune détection de port série.")
            return None

        print(f"Connexion en cours avec l'Arduino sur le port {port}...")
        board = pyfirmata2.Arduino(port)
        print(f"Connecté avec succès à l'Arduino sur {port}.")
        return board

    except IOError as e:
        print(f"Erreur de connexion à l'Arduino : {e}")
        return None
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return None

# Appel de la fonction
board = connect_to_arduino()

if board:
    print("L'Arduino est prêt à être utilisé.")
else:
    print("Impossible de connecter l'Arduino.")
