import threading
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from app.config import get_network
from app.monitor import compare_devices
from app.scanner import scan_network , cancel_event
from app.storage import load_devices_from_last_scan, save_devices
from app.pdf_report import generate_pdf


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
        
        self.progress = ttk.Progressbar(
            self, orient="horizontal", length=300,mode="indeterminate"
        )
        self.progress.pack(pady=10)

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
        
        ttk.Button(botoes,text= "Gerar PDF", command=self.salvar_pdf).pack(
            side="left",padx=10
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
        
            if not self.monitorando:
                break

            self.master.after(
                0, lambda: [self.status.config(text="Escaneando..."),
                self.progress.start(10),],
            )
            dispositivos = scan_network(self.network)
            
            if not self.monitorando:
                break

            save_devices(dispositivos)

            novos, removidos = compare_devices(antigos, dispositivos)

            
            if self.monitorando:
                self.master.after(
                    0,
                    lambda: [
                        self.progress.stop(),
                        self.atualizar_tabela(dispositivos,novos,removidos)
                    ]
                )

            for _ in range(5):
                if not self.monitorando:
                    break
                time.sleep(1)

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
    
    def salvar_pdf(self,*args):
        try:
            generate_pdf()  

            messagebox.showinfo(
                "Sucesso",
                "Relatório PDF gerado com sucesso!"
            )
        except Exception as e:
            messagebox.showerror("ERRO",f"Não foi possível salvar em PDF.\n{e}\n")

    def parar(self):
        self.monitorando = False
        cancel_event.set()
        self.progress.stop()
        self.status.config(text="Status: Parado")

    def voltar(self):
        from .control_panel import Control_panel

        self.monitorando = False
        cancel_event.set()
        self.progress.stop()
        self.destroy()
        Control_panel(self.master)
    
    def _finalizar_voltar(self):
        from .control_panel import Control_panel
        self.destroy()
        Control_panel(self.master)