from tkinter import *
from tkinter import ttk
from tkinter import messagebox
class ReportScreen(ttk.Frame):
    def __init__(self,master):
        
        super().__init__(master)
        self.master = master
        self.pack(fill="both",expand=True)
        
        self.create_widgets()
        self.load_report_data()
        
    def create_widgets(self):
        
        ttk.Label(
            self,text="REPORT PANEL", font=("Arial",20,"bold")
        ).pack(pady=15)
        
        filter_frame = ttk.LabelFrame(self, text = " Filters ")
        filter_frame.pack(fill="x",padx=20,pady=5)
        
        ttk.Label(filter_frame,text="Period:").pack(side="left",padx=5,pady=5)
        self.period_combo = ttk.Combobox(
            filter_frame, values = ["All history", "Lasts 24 Hours", "Last 7 Days"], state = "reandoly"
        )
        self.period_combo.current(0)
        self.period_combo.pack(side="left",padx=5,pady=5)
        
        ttk.Button(filter_frame, text = "Apply Filter", command=self.apply_filter).pack(side="left",padx=10)
        
        stats_frame = ttk.Frame(self)
        stats_frame.pack(fill="x",padx=20,pady=10)
        
        self.lbl_total_scans = ttk.Label(stats_frame, text = "Total scans: --",font=("Arial",11,"bold"))
        self.lbl_total_scans.pack(side="left",padx=20)
        
        self.lbl_total_devices = ttk.Label(stats_frame,text = "Devices Tracked: --", font=("Arial", 11, "bold"))
        self.lbl_total_scans.pack(side="left",padx=20)
        
        self.report_tree = ttk.Treeview(
            self,
            columns=("ID","TIMESTAMP","DEVICES_ONLINE"),
            show="headings",
            height=12
        )
        self.report_tree.heading("ID",text="Scan ID")
        self.report_tree.heading("TIMESTAMP", text="Date & Time")
        self.report_tree.heading("DEVICES_ONLINE", text="Devices Online")
        
        self.report_tree.column("ID",width=80,anchor="center")
        self.report_tree.column("TIMESTAMP",width=250,anchor="center")
        self.report_tree.column("DEVICES_ONLINE",width=150,anchor="center")
        
        self.report_tree.pack(fill="both",expand=True,padx=20,pady=10)
        
        self.report_tree.bind("<<TreeViewSelect>>",self.on_scan_selected)
        
        actions_frame=ttk.Frame(self)
        actions_frame.pack(pady=15)
        
        ttk.Button(actions_frame,text="Export PDF Report", command=self.export_pdf)
        ttk.Button(actions_frame,text="Back",command=self.voltar).pack(side="left",padx=10)
        
    
    def load_report_data(self):
        self.lbl_total_scans.config(text="Total scans: 14")
        self.lbl_total_devices.config(text="Devices Tracked: 8")
        
        self.report_tree.delete(*self.report_tree.get_children())
        
    def apply_filter(self):
        selected = self.period_combo.get()
        print(f"Filtering by: {selected}")
    
    def on_scan_selected(self,event):
        selected_item = self.report_tree.selection()
        if selected_item:
            item_data = self.report_tree.item(selected_item,"values")
            print(f"Selected Scan ID: {item_data[0]}")
        
    
    def export_pdf(self):
        messagebox.showinfo("Export","Generating PDF Report...")
    
    def voltar(self):
        from .control_panel import Control_panel
        self.destroy()
        Control_panel(self.master)
        

        
        
        
        
        
    