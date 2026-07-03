from tkinter import ttk
from .monitor_screen import MonitorScreen


class Control_panel(ttk.Frame):
    
    def __init__(self,master):
        
        super().__init__(master)
        
        self.pack(fill="both",expand=True)
        
        self.create_widgets()
        
    def create_widgets(self):
        
        ttk.Label(
            self,
            text="Monitoramento de dispositivos de rede",
            font=("Arial,12"),
            ).pack    
        
        ttk.Separator(self).pack(fill="x", padx=50,pady=25)
        
        ttk.Button(
            self,
            text="Iniciar monitoramento",
            width = 35,
            command = self.abrir_monitor
        ).pack(pady=10)
        
        ttk.Button(
            self,
            text = "Historico",
            width = 35
        ).pack(pady=10)
      
        ttk.Button(
            self,
            text = "Relatórios",
            width = 35
        ).pack(pady=10)
        
        ttk.Button(
            self,
            text = "Sair",
            width = 35
        ).pack(pady=10)
        
    def abrir_monitor(self):
        
        self.destroy()
        
        MonitorScreen(self.master)
    