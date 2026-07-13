# 🌐 Network Monitor

A cross-platform network monitoring application developed in Python for local area networks (LANs). The system periodically scans a configurable subnet, detects connected devices, identifies their operating systems, hardware vendors (through MAC addresses), and collects information about network services.

All collected data is stored in a local SQLite relational database, allowing historical tracking of network devices, event logging, and automated PDF report generation.

---

## ✨ Features

- ⚡ **Parallel Network Scanning**
  - Uses `ThreadPoolExecutor` with **Nmap** to efficiently scan multiple hosts simultaneously.

- 🖥️ **Device Discovery**
  - Detects:
    - IP Address
    - MAC Address
    - Hostname
    - Vendor
    - Operating System
    - Device Status

- 🗄️ **SQLite Database**
  - Stores every scan in a relational database.
  - Maintains historical records of devices and scans.

- 🔄 **Real-Time Monitoring**
  - Detects:
    - New devices joining the network.
    - Devices that become unavailable.

- 📄 **PDF Report Generation**
  - Generates detailed PDF reports containing information about the latest scan.

- 📝 **Event Logging**
  - Stores monitoring events in log files for auditing and troubleshooting.

- 🖥️ **Desktop Interface**
  - Simple graphical interface built with **Tkinter** for starting scans, monitoring devices, and generating reports.

- 🌍 **Cross-Platform**
  - Compatible with:
    - Windows
    - Linux
    - macOS

---

# 📂 Project Structure

```text
network_monitor/
│
├── app/
│   ├── config.py          # Application configuration
│   ├── logger.py          # Event logging
│   ├── main.py            # Application entry point
│   ├── monitor.py         # Device comparison logic
│   ├── pdf_report.py      # PDF report generator
│   ├── scanner.py         # Nmap network scanner
│   ├── storage.py         # SQLite database operations
│   └── utils.py           # Utility functions
│
├── gui/
│   ├── control_panel.py
│   ├── dashboard.py
│   ├── history_screen.py
│   ├── monitor_screen.py
│   ├── reports_screen.py
│   └── settings_screen.py
│
├── data/
│   └── network_monitor.db     # SQLite database (auto-generated)
│
├── history/
│   └── report_*.pdf           # Generated reports
│
├── logs/
│   └── monitor.log            # Application logs
│
├── requirements.txt
├── .env
└── README.md
```

---

# 📋 Requirements

- Python **3.10+**
- Nmap installed on your operating system
- Git (optional)

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/your-user/network_monitor.git
```

Go to the project folder:

```bash
cd network_monitor
```

Create a virtual environment:

### Windows

```bash
py -m venv .venv
```

### Linux / macOS

```bash
python3 -m venv .venv
```

Activate the virtual environment.

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

# ⚙️ Configuration

Create a `.env` file in the project root.

Example:

```env
NETWORK=192.168.1.0/24
```

If supported by your operating system, the application can also automatically detect the local network.

---

# ▶️ Running

```bash
python app/main.py
```

---

# 📄 Generated Files

During execution, the application automatically creates:

- `data/network_monitor.db`
- `logs/monitor.log`
- `history/report_<timestamp>.pdf`

---

# 🛠️ Technologies

- Python
- Tkinter
- SQLite
- python-nmap
- ReportLab
- python-dotenv
- ThreadPoolExecutor

---

# 📈 Future Improvements

- Network topology visualization
- Interactive dashboard with charts
- Email notifications
- SNMP monitoring
- REST API
- Multi-user authentication
- Device inventory management
- Export reports to Excel
- Dark mode interface

---

# 📜 License

This project is licensed under the MIT License.
