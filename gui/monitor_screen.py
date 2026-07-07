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
        self.monitoring = False

        
        self.status = ttk.Label(self, text="Status: Stopped")

        if not self.network:
            self.status.config(text="Network not found")
            self.status.pack(pady=20)
            return

        self.create_widgets()

    def create_widgets(self):

        ttk.Label(
            self, text="NETWORK MONITORING", font=("Arial", 20, "bold")
        ).pack(pady=15)

        
        self.status.pack()
        
        self.progress = ttk.Progressbar(
            self, orient="horizontal", length=300,mode="indeterminate"
        )
        self.progress.pack(pady=10)

        self.tree = ttk.Treeview(
            self,
            columns=("IP", "HOST", "OS", "VENDOR"),
            show="headings",
            height=20,
        )

        self.tree.heading("IP", text="IP")
        self.tree.heading("HOST", text="Hostname")
        self.tree.heading("OS", text="Operation System")
        self.tree.heading("VENDOR", text="Vendor")

        self.tree.column("IP", width=150)
        self.tree.column("HOST", width=220)
        self.tree.column("OS", width=220)
        self.tree.column("VENDOR", width=220)

        self.tree.pack(fill="both", expand=True, padx=15, pady=20)

        botoes = ttk.Frame(self)
        botoes.pack(pady=10)

        ttk.Button(botoes, text="Start", command=self.start).pack(
            side="left", padx=10
        )
        ttk.Button(botoes, text="Stop", command=self.stop).pack(
            side="left", padx=10
        )
        ttk.Button(botoes, text="Back", command=self.back).pack(
            side="left", padx=10
        )
        
        ttk.Button(botoes,text= "Generate PDF", command=self.save_pdf).pack(
            side="left",padx=10
        )

        ttk.Label(self, text="Events").pack()

        self.log = Text(self, height=8)
        self.log.pack(fill="x", padx=20)

    def start(self):
        if self.monitoring:
            return

        self.monitoring = True

        threading.Thread(target=self.monitor, daemon=True).start()

    def monitor(self):

        while self.monitoring:
            olds = load_devices_from_last_scan()
        
            if not self.monitoring:
                break

            self.master.after(
                0, lambda: [self.status.config(text="Scanning..."),
                self.progress.start(10),],
            )
            devices = scan_network(self.network)
            
            if not self.monitoring:
                break

            save_devices(devices)

            new, removed = compare_devices(olds, devices)

            
            if self.monitoring:
                self.master.after(
                    0,
                    lambda: [
                        self.progress.stop(),
                        self.update_table(devices,new,removed)
                    ]
                )

            for _ in range(5):
                if not self.monitoring:
                    break
                time.sleep(1)

    def update_table(self, devices, new, removed):
       
        self.tree.delete(*self.tree.get_children())

        
        for d in devices:
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
            text=f"Status: Monitoring ({len(devices)} dispositivos)"
        )

       
        self.log.delete("1.0", END)

        timestamp = time.strftime("%H:%M:%S")

        for ip in new:
            self.log.insert(END, f"[{timestamp}] [NEW] {ip}\n")
        for ip in removed:
            self.log.insert(END, f"[{timestamp}] [OFFLINE] {ip}\n")

        if not new and not removed:
            self.log.insert(END, f"[{timestamp}] Nothing changes.\n")

        
        self.log.see(END)
    
    def save_pdf(self,*args):
        try:
            generate_pdf()  

            messagebox.showinfo(
                "Success",
                "Report PDF generated!"
            )
        except Exception as e:
            messagebox.showerror("ERROR",f"Unable to save as PDF.\n{e}\n")

    def stop(self):
        self.monitorando = False
        cancel_event.set()
        self.progress.stop()
        self.status.config(text="Status: Stopped")

    def back(self):
        from .control_panel import Control_panel

        self.monitoring = False
        cancel_event.set()
        self.progress.stop()
        self.destroy()
        Control_panel(self.master)
    
    def _finish_back(self):
        from .control_panel import Control_panel
        self.destroy()
        Control_panel(self.master)