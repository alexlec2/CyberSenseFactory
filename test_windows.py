import pyfirmata2
import time

def main():
    # Remplacez "COM3" par le port série de votre Arduino
    port = pyfirmata2.Arduino.AUTODETECT  # Auto-détection du port
    print("Recherche du port Arduino...")
    board = pyfirmata2.Arduino(port)
    print(f"Connecté à l'Arduino sur le port : {port}")

    # Initialisation de la LED (par exemple sur la broche 13)
    led_pin = 13
    board.digital[led_pin].mode = pyfirmata2.OUTPUT

    # Configuration pour lire une broche analogique (exemple A0)
    analog_pin = 0

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

            # Lire une valeur analogique
            analog_value = board.analog[analog_pin].read()
            if analog_value is not None:
                print(f"Valeur analogique (A0): {analog_value}")
            
    except KeyboardInterrupt:
        print("\nProgramme interrompu par l'utilisateur.")
    finally:
        board.exit()  # Déconnecter proprement l'Arduino
        print("Arduino déconnecté.")

if __name__ == "__main__":
    main()
