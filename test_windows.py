import pyfirmata2
import time
import serial.tools.list_ports


def main():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(port)
    # Spécifiez le port COM auquel votre Arduino est connecté
    port = pyfirmata2.Arduino.AUTODETECT  # Vous pouvez spécifier "COM3" ou "COMx" directement
    print(f"Tentative de connexion à l'Arduino sur le port : {port}")

    # Connectez-vous à l'Arduino
    try:
        board = pyfirmata2.Arduino(port)
        print(f"Connecté à l'Arduino sur {port}.")
    except Exception as e:
        print(f"Impossible de se connecter à l'Arduino. Vérifiez le port et essayez à nouveau.\nErreur : {e}")
        return

    # Configuration d'une broche pour démonstration
    led_pin = 13  # Broche numérique pour la LED
    board.digital[led_pin].mode = pyfirmata2.OUTPUT

    try:
        while True:
            # Allumer la LED
            print("LED ON")
            board.digital[led_pin].write(1)
            time.sleep(1)  # Attendre 1 seconde

            # Éteindre la LED
            print("LED OFF")
            board.digital[led_pin].write(0)
            time.sleep(1)  # Attendre 1 seconde

    except KeyboardInterrupt:
        print("\nProgramme interrompu par l'utilisateur.")
    finally:
        board.exit()  # Fermer correctement la connexion
        print("Connexion à l'Arduino terminée.")

if __name__ == "__main__":
    main()
