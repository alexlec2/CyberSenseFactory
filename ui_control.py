from tkinter import Tk
from tkinterElements import create_scada_frames, create_config_frame
from tkinter import Frame, Button
from base import connect_to_arduino, disconnect_from_arduino, init_relay_output

time_sleep = 0.5
board = None
relays = [[13, 12], [8, 7], [4, 2]]

def toggle_view(scada_frame, config_frame):

    if scada_frame.winfo_viewable():
        scada_frame.pack_forget()
        config_frame.pack(fill='both', expand=True)
    else:
        config_frame.pack_forget()
        scada_frame.pack(fill='y', expand=True)

def create_ui():
    root = Tk()
    root.title("Scada CyberSense Factory")
    root.geometry("800x600")

    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.columnconfigure(0, weight=1, minsize=800)
    
    board = connect_to_arduino()
    init_relay_output(board, relays)
    
    margin = 10

    scada_frame = Frame(root, bg="white")
    scada_frame.pack(fill='y', expand=True)

    ui_elements, status_label = create_scada_frames(board, scada_frame, relays, margin, time_sleep)
    status_label.config(text="Connecté à l'Arduino.", foreground="green")

    config_frame = Frame(root, bg="white")
    config_frame.pack(fill='both', expand=True)

    create_config_frame(config_frame, relays, board)

    switch_frame_button = Button(
        root, 
        text="\u2630",
        bg="white",
        activebackground="lightgray",
        width=2,
        height=1,
        command=lambda: toggle_view(scada_frame, config_frame),
        state="normal"
    )
    switch_frame_button.place(relx=1, rely=0, x=-30, y=10, anchor="ne")
    ui_elements.append(switch_frame_button)
    
    config_frame.pack_forget()

    root.mainloop()

if __name__ == "__main__":
    create_ui()
    disconnect_from_arduino(board)
