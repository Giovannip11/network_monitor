import os
import sqlite3
from datetime import datetime

DATA_DIR = r"C:/projetos/network_monitor/data"
DB_PATH = os.path.join(DATA_DIR, "network_monitor.db")

os.makedirs(DATA_DIR, exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        # Table: devices
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS devices
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL,
                mac TEXT,
                name TEXT,
                vendor TEXT,
                os TEXT
            )
            """
        )

        # Table: scan_history
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL
            )
            """
        )

        # Table: device_logs
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS device_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER NOT NULL,
                device_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (scan_id) REFERENCES scan_history(id) ON DELETE CASCADE,
                FOREIGN KEY (device_id) REFERENCES devices(id)
            )
            """
        )
        conn.commit()


def save_devices(devices_list):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Gets current local user time dynamically
        local_time = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO scan_history (timestamp) VALUES (?)", (local_time,)
        )
        scan_id = cursor.lastrowid

        for dev in devices_list:
            cursor.execute("SELECT id FROM devices WHERE ip = ?", (dev.get("ip"),))
            row = cursor.fetchone()

            name = dev.get("hostname", "Unknown")
            vendor = dev.get("vendor", "Unknown")
            os_name = dev.get("os", "Unknown")

            if row:
                device_id = row["id"]

                cursor.execute(
                    """
                        UPDATE devices
                        SET name = ?, vendor = ?, os = ?
                        WHERE id = ?
                    """,
                    (name, vendor, os_name, device_id),
                )
            else:
                cursor.execute(
                    """
                        INSERT INTO devices(ip, mac, name, vendor, os)
                        VALUES(?,?,?,?,?)
                    """,
                    (dev.get("ip"), dev.get("mac"), name, vendor, os_name),
                )
                device_id = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO device_logs (scan_id, device_id, status)
                VALUES (?, ?, ?)
                """,
                (scan_id, device_id, dev.get("status", "Online")),
            )
        conn.commit()


def load_devices_from_last_scan():
    with get_connection() as conn:
        cursor = conn.cursor()

        query = """
            SELECT
                d.ip,
                d.name as hostname,
                d.vendor,
                d.os,
                h.timestamp as data_hora, -- Kept as alias to not break your UI template
                l.status
            FROM device_logs l
            JOIN devices d ON l.device_id = d.id
            JOIN scan_history h ON l.scan_id = h.id
            WHERE l.scan_id = (SELECT MAX(id) FROM scan_history)
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        return [dict(row) for row in rows]