import sqlite3

class MedicationService:
    def __init__(self):
        self.database_url = "data/medications.db"
        self.setup_db()

    def setup_db(self):
        """Creates the database if it does not exist yet."""
        conn = sqlite3.connect(self.database_url)
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

    def create_medication(self, name, dosage):
        """Inserts medication into the database"""
        conn = sqlite3.connect(self.database_url)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO medications (name, dosage)
            VALUES (?, ?)
        """, (name, dosage))

        conn.commit()
        conn.close()

    def delete_medication(self, name, dosage):
        """Deletes medication from the database"""
        conn = sqlite3.connect(self.database_url)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM medications
            WHERE name = ? AND dosage = ?
        """, (name, dosage))

        conn.commit()

        deleted_rows = cursor.rowcount

        conn.close()

        return deleted_rows > 0

    def get_medication_by_name(self, name):
        """Reads medication by name from the database"""
        conn = sqlite3.connect(self.database_url)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM medications
            WHERE name = ?
        """, (name,))

        result = cursor.fetchall()

        conn.close()

        return result

    def get_medication_by_dosage(self, dosage):
        """Reads medication by dosage from the database"""
        conn = sqlite3.connect(self.database_url)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM medications
            WHERE dosage = ?
        """, (dosage,))

        result = cursor.fetchall()

        conn.close()

        return result

    def get_medication_by_name_and_dosage(self, name, dosage):
        """Reads medication by name and dosage from the database"""
        conn = sqlite3.connect(self.database_url)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM medications
            WHERE name = ? AND dosage = ?
        """, (name, dosage))
        result = cursor.fetchall()

        conn.close()

        return result

    def get_all_medications(self):
        """Reads all medications from the database"""
        conn = sqlite3.connect(self.database_url)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM medications")
        result = cursor.fetchall()

        conn.close()

        return result