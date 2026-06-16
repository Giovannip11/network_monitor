import os
import sqlite3

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
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS dispositivos
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL,
                mac TEXT UNIQUE,
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
                data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
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
        
        cursor.execute("INSERT INTO historico_varreduras DEFAULT VALUES ")
        id_varredura = cursor.lastrowid
        
        for dev in devices_list:
           
            cursor.execute("SELECT id FROM dispositivos WHERE ip = ?", (dev.get('ip'),))
            row = cursor.fetchone()
            
            
            nome = dev.get('hostname', 'Desconhecido')
            fabricante = dev.get('vendor', 'Desconhecido')
            so = dev.get('os', 'Desconhecido')
            
            if row:
                id_dispositivo = row['id']
                
                cursor.execute(
                    """
                        UPDATE dispositivos
                        SET nome = ?, fabricante = ?, so = ?
                        WHERE id = ?
                    """,
                    (nome, fabricante, so, id_dispositivo)
                )
            else:
                cursor.execute(
                    """
                        INSERT INTO dispositivos(ip, mac, nome, fabricante, so)
                        VALUES(?,?,?,?,?)
                    """,
                    (dev.get('ip'), dev.get('mac'), nome, fabricante, so)
                )
                id_dispositivo = cursor.lastrowid
                
            
            cursor.execute(
                """
                INSERT INTO logs_dispositivos (id_varredura, id_dispositivo, status)
                VALUES (?, ?, ?)
                """, 
                (id_varredura, id_dispositivo, dev.get('status', 'Online'))
            )
        conn.commit()
        
def load_devices_from_last_scan():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        query = """
            SELECT d.ip, d.nome as hostname, d.fabricante as vendor, d.so as os, h.data_hora, l.status
            FROM logs_dispositivos l
            JOIN dispositivos d ON l.id_dispositivo = d.id
            JOIN historico_varreduras h ON l.id_varredura = h.id
            WHERE l.id_varredura = (SELECT MAX(id) FROM historico_varreduras)
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]