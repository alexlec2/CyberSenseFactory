import time

def activate_relay(board, relay_pin, last_activated_relay):
    """Active le relais spécifié pendant 0,5 seconde si ce n'était pas le dernier activé."""
    print(last_activated_relay, relay_pin)
    if last_activated_relay != relay_pin:  # Activer seulement si ce n'était pas le dernier relais activé
        print(f"Activation du relais {relay_pin}.")
        board.digital[relay_pin].write(1)
        time.sleep(0.5)
        board.digital[relay_pin].write(0)
        print(f"Relais {relay_pin} désactivé.")
        last_activated_relay = relay_pin
    else:
        print(f"Relais {relay_pin} n'a pas été activé car c'est déjà le dernier activé.")
