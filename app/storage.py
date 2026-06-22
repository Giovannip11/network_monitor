import os
import sqlite3
from datetime import datetime, timedelta, timezone

DATA_DIR = r"C:/projetos/network_monitor/data"
DB_PATH = os.path.join(DATA_DIR, "network_monitor.db")

os.makedirs(DATA_DIR, exist_ok=True)
FUSO_LOCAL = timezone(timedelta(hours=-3))


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS dispositivos
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL,
                mac TEXT ,
                nome TEXT,
                fabricante TEXT,
                so TEXT
            )
            """
        )

        cursor.execute(
            """
           CREATE TABLE IF NOT EXISTS historico_varreduras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS logs_dispositivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_varredura INTEGER NOT NULL,
                id_dispositivo INTEGER NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (id_varredura) REFERENCES historico_varreduras(id) ON DELETE CASCADE,
                FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id)
            )
            """
        )
        conn.commit()


def save_devices(devices_list):
    with get_connection() as conn:
        cursor = conn.cursor()

        agora_local = datetime.now(FUSO_LOCAL).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO historico_varreduras (data_hora) VALUES (?)", (agora_local,)
        )
        id_varredura = cursor.lastrowid

        for dev in devices_list:
            cursor.execute("SELECT id FROM dispositivos WHERE ip = ?", (dev.get("ip"),))
            row = cursor.fetchone()

            nome = dev.get("hostname", "Desconhecido")
            fabricante = dev.get("vendor", "Desconhecido")
            so = dev.get("os", "Desconhecido")

            if row:
                id_dispositivo = row["id"]

                cursor.execute(
                    """
                        UPDATE dispositivos
                        SET nome = ?, fabricante = ?, so = ?
                        WHERE id = ?
                    """,
                    (nome, fabricante, so, id_dispositivo),
                )
            else:
                cursor.execute(
                    """
                        INSERT INTO dispositivos(ip, mac, nome, fabricante, so)
                        VALUES(?,?,?,?,?)
                    """,
                    (dev.get("ip"), dev.get("mac"), nome, fabricante, so),
                )
                id_dispositivo = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO logs_dispositivos (id_varredura, id_dispositivo, status)
                VALUES (?, ?, ?)
                """,
                (id_varredura, id_dispositivo, dev.get("status", "Online")),
            )
        conn.commit()


def load_devices_from_last_scan():
    with get_connection() as conn:
        cursor = conn.cursor()

        query = """
            SELECT
                d.ip,
                d.nome as hostname,
                d.fabricante as vendor,
                d.so as os,
                datetime(h.data_hora, 'localtime') as data_hora,
                l.status
            FROM logs_dispositivos l
            JOIN dispositivos d ON l.id_dispositivo = d.id
            JOIN historico_varreduras h ON l.id_varredura = h.id
            WHERE l.id_varredura = (SELECT MAX(id) FROM historico_varreduras)
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        return [dict(row) for row in rows]
