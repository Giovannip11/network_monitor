from tkinter import *
from tkinter import ttk

class SettingsScreen(ttk.Frame):
    def __init__(self,master):
        
        super().__init__(master)
        self.master = master
        self.pack(fill="both",expand=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        ttk.Label(
            self,text="Settings", font=("Arial",20, "bold")
        ).pack(pady=15)
        