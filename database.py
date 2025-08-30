import sqlite3
import os
import sys

def _get_base_dir():
    # When running as exe via PyInstaller
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)
    # During development
    return os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(_get_base_dir(), "flights.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                flight_number TEXT NOT NULL,
                departure TEXT NOT NULL,
                destination TEXT NOT NULL,
                date TEXT NOT NULL,
                seat_number TEXT NOT NULL
            );
        """)
        conn.commit()

def add_reservation(name, flight_number, departure, destination, date, seat_number):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO reservations (name, flight_number, departure, destination, date, seat_number)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, flight_number, departure, destination, date, seat_number))
        conn.commit()
        return cur.lastrowid

def get_all_reservations():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, flight_number, departure, destination, date, seat_number FROM reservations ORDER BY id DESC;")
        return cur.fetchall()

def get_reservation_by_id(res_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, flight_number, departure, destination, date, seat_number FROM reservations WHERE id=?;", (res_id,))
        return cur.fetchone()

def update_reservation(res_id, name, flight_number, departure, destination, date, seat_number):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE reservations
            SET name=?, flight_number=?, departure=?, destination=?, date=?, seat_number=?
            WHERE id=?
        """, (name, flight_number, departure, destination, date, seat_number, res_id))
        conn.commit()
        return cur.rowcount

def delete_reservation(res_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM reservations WHERE id=?;", (res_id,))
        conn.commit()
        return cur.rowcount
