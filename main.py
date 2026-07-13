import os
from tkinter import *
from tkinter import ttk

from app.config import get_network
from app.storage import init_db
from gui.control_panel import Control_panel


def main():

    print("Initializing database...")
    init_db()


    network = get_network()
    if network is None:
        print("Error: Could not automatically detect local network.")

    else:
        print(f"Network detected: {network}")


    print("Starting Graphic Interface...")
    root = Tk()
    root.title("Network Monitor v1.0")
    root.geometry("900x650")


    Control_panel(root)


    root.mainloop()


if __name__ == "__main__":
    main()
