import os
import sqlite3

from config import DATABASE_PATH

def initialize_db():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_metadata (
            id INTEGER PRIMARY KEY,
            session_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            submission_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            expiration_time DATETIME
        )
        ''')

def insert_metadata(session_id, filename, status, expiration_time):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO file_metadata (session_id, filename, status, expiration_time) 
        VALUES (?, ?, ?, ?)
        ''', (session_id, filename, status, expiration_time))
