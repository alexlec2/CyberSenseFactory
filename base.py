from pyfirmata2 import Arduino

def connect_to_arduino():
    try:
        port = Arduino.AUTODETECT
        board = Arduino(port)
        return board
    except IOError as e:
        return None

def disconnect_from_arduino(board):
    if board:
        board.exit()

def init_relay_output(board, relays):
    for relay in relays:
        for output in relay:
            board.digital[output].mode = 1
            if output == 4 or output == 2:
                board.digital[output].write(1)
            else:
                board.digital[output].write(0)
