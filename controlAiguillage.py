import time

def activate_relay(board, relay_pin, time_sleep):
    """Active le relais spécifié pendant 0,5 seconde."""
    print(f"Activation du relais {relay_pin}.")
    board.digital[relay_pin].write(1)
    time.sleep(time_sleep)
    board.digital[relay_pin].write(0)
    print(f"Relais {relay_pin} désactivé.")
