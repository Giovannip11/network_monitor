from tkinter import ttk
from tkinter import *
import platform
import os
import subprocess
from app.pdf_report import *
from gui.settings import SettingsScreen
from .monitor_screen import MonitorScreen
from .reports import ReportScreen
class Control_panel(ttk.Frame):

    def __init__(self,master):

        super().__init__(master)

        self.pack(fill="both",expand=True)

        self.create_widgets()

    def create_widgets(self):

        ttk.Label(
            self,
            text="Network device monitoring",
            font=("Arial,12"),
            ).pack()

        ttk.Separator(self).pack(fill="x", padx=50,pady=25)

        ttk.Button(
            self,
            text="Start",
            width = 35,
            command = self.open_monitor
        ).pack(pady=10)

        ttk.Button(
            self,
            text = "History",
            width = 35,
            command= self.open_history
        ).pack(pady=10)

        ttk.Button(
            self,
            text = "Reports",
            width = 35,
            command= self.open_report
        ).pack(pady=10)

        ttk.Button(
             self,
             text= "Settings",
             width= 35,
             command= self.open_settings
         ).pack(pady=10)

        ttk.Button(
            self,
            text = "Exit",
            width = 35,
            command = self.master.destroy
        ).pack(pady=10)



    def open_monitor(self):

        self.destroy()

        MonitorScreen(self.master)
    def open_report(self):
        self.destroy()

        ReportScreen(self.master)

    def open_settings(self):
        self.destroy()
        SettingsScreen(self.master)

    def open_history(self):
        if platform.system() == "Windows":
            os.startfile(HISTORY_DIR)

        elif platform.system() == "Linux":
            subprocess.run(["xdg-open",HISTORY_DIR])
