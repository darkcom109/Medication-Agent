import sqlite3

def setup_db():
    conn = sqlite3.connect("database/medications.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dosage TEXT NOT NULL               
        )
    """)

    conn.commit()
    conn.close()

def create_medication(name, dosage):
    conn = sqlite3.connect("database/medications.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO medications (name, dosage)
        VALUES (?, ?)
    """, (name, dosage))

    conn.commit()
    conn.close()

def get_all_medications():
    conn = sqlite3.connect("database/medications.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medications")
    result = cursor.fetchall()

    conn.close()
    return result