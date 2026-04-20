import sqlite3

def setup_db():
    """Creates the database if it does not exist yet."""
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
    """Inserts medication into the database"""
    conn = sqlite3.connect("database/medications.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO medications (name, dosage)
        VALUES (?, ?)
    """, (name, dosage))

    conn.commit()
    conn.close()

def delete_medication(name, dosage):
    """Deletes medication from the database"""
    conn = sqlite3.connect("database/medications.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM medications
        WHERE name = ? AND dosage = ?
    """, (name, dosage))

    conn.commit()
    conn.close()

def get_medication_by_name(name):
    """Reads medication by name from the database"""
    conn = sqlite3.connect("database/medications.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM medications
        WHERE name = ?
    """, (name,))

    result = cursor.fetchall()

    conn.close()

    return result

def get_medication_by_dosage(dosage):
    """Reads medication by dosage from the database"""
    conn = sqlite3.connect("database/medications.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT dosage FROM medications
        WHERE dosage = ?
    """, (dosage,))

    result = cursor.fetchall()

    conn.close()

    return result

def get_medication_by_name_and_dosage(name, dosage):
    """Reads medication by name and dosage from the database"""
    conn = sqlite3.connect("database/medications.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM medications
        WHERE name = ? AND dosage = ?
    """, (name, dosage))
    result = cursor.fetchall()

    conn.close()

    return result

def get_all_medications():
    """Reads all medications from the database"""
    conn = sqlite3.connect("database/medications.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medications")
    result = cursor.fetchall()

    return result