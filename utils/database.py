import sqlite3
from datetime import datetime

DB_NAME = "history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT,
            confidence REAL,
            timestamp TEXT,
            processing_time REAL
        )
    """)

    conn.commit()
    conn.close()


def insert_record(plate, confidence, processing_time):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO history (plate, confidence, timestamp, processing_time)
        VALUES (?, ?, ?, ?)
        """,
        (
            plate,
            confidence,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            processing_time
        )
    )

    conn.commit()
    conn.close()



def fetch_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT plate, confidence, timestamp, processing_time
        FROM history
        ORDER BY id DESC
        """
    )
    rows = cursor.fetchall()

    conn.close()
    return rows


def clear_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history")

    conn.commit()
    conn.close()

