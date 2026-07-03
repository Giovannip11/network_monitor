import threading
import time
from tkinter import *
from tkinter import ttk

from app.config import get_network
from app.monitor import compare_devices
from app.scanner import scan_network
from app.storage import load_devices_from_last_scan, save_devices


class MonitorScreen(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.pack(fill="both", expand=True)

        
        self.network = get_network()
        self.monitorando = False

      
        self.status = ttk.Label(self, text="Status: Parado")

        if not self.network:
            self.status.config(text="Rede não encontrada")
            self.status.pack(pady=20)
            return

        self.create_widgets()

    def create_widgets(self):

        ttk.Label(
            self, text="MONITORAMENTO DA REDE", font=("Arial", 20, "bold")
        ).pack(pady=15)

        
        self.status.pack()

        self.tree = ttk.Treeview(
            self,
            columns=("IP", "HOST", "SO", "FABRICANTE"),
            show="headings",
            height=20,
        )

        self.tree.heading("IP", text="IP")
        self.tree.heading("HOST", text="Hostname")
        self.tree.heading("SO", text="Sistema operacional")
        self.tree.heading("FABRICANTE", text="Fabricante")

        self.tree.column("IP", width=150)
        self.tree.column("HOST", width=220)
        self.tree.column("SO", width=220)
        self.tree.column("FABRICANTE", width=220)

        self.tree.pack(fill="both", expand=True, padx=15, pady=20)

        botoes = ttk.Frame(self)
        botoes.pack(pady=10)

        ttk.Button(botoes, text="Iniciar", command=self.iniciar).pack(
            side="left", padx=10
        )
        ttk.Button(botoes, text="Parar", command=self.parar).pack(
            side="left", padx=10
        )
        ttk.Button(botoes, text="Voltar", command=self.voltar).pack(
            side="left", padx=10
        )

        ttk.Label(self, text="Eventos").pack()

        self.log = Text(self, height=8)
        self.log.pack(fill="x", padx=20)

    def iniciar(self):
        if self.monitorando:
            return

        self.monitorando = True

        threading.Thread(target=self.monitor, daemon=True).start()

    def monitor(self):

        while self.monitorando:
            antigos = load_devices_from_last_scan()

            self.master.after(
                0, lambda: self.status.config(text="Escaneando...")
            )
            dispositivos = scan_network(self.network)

            save_devices(dispositivos)

            novos, removidos = compare_devices(antigos, dispositivos)

            
            if self.monitorando:
                self.master.after(
                    0,
                    lambda: self.atualizar_tabela(
                        dispositivos, novos, removidos
                    ),
                )

            time.sleep(5)

    def atualizar_tabela(self, dispositivos, novos, removidos):
       
        self.tree.delete(*self.tree.get_children())

        
        for d in dispositivos:
            self.tree.insert(
                "",
                "end",
                values=(
                    d.get("ip", ""),
                    d.get("hostname", ""),
                    d.get("os", ""),
                    d.get("vendor", ""),
                ),
            )

        self.status.config(
            text=f"Status: Monitorando ({len(dispositivos)} dispositivos)"
        )

       
        self.log.delete("1.0", END)

        timestamp = time.strftime("%H:%M:%S")

        for ip in novos:
            self.log.insert(END, f"[{timestamp}] [NOVO] {ip}\n")
        for ip in removidos:
            self.log.insert(END, f"[{timestamp}] [OFFLINE] {ip}\n")

        if not novos and not removidos:
            self.log.insert(END, f"[{timestamp}] Nenhuma mudança.\n")

        
        self.log.see(END)

    def parar(self):
        self.monitorando = False
        self.status.config(text="Status: Parado")

    def voltar(self):
        .from control_panel import Control_panel

        self.monitorando = False
        self.destroy()
        Control_panel(self.master)
