import sqlite3

class DatabaseManager:
    def __init__(self, db_name="database.db"):
        """Initialize the database connection."""
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Enforce foreign key constraints
        self.cursor.execute("PRAGMA foreign_keys = ON")

    def create_table(self, table_name):
        """
        Create a table with a fixed size of 16 entries.
        If more than 16 entries exist, the oldest one will be removed.
        """
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
        self.cursor.execute(query)
        self.conn.commit()

    def insert(self, table_name, content):
        """
        Insert a new entry into the table. If the table exceeds 16 rows,
        the oldest entry (smallest id) is deleted automatically.

        Args:
            table_name (str): Name of the table.
            content (str): Clipboard content (text, image path, etc.).
        """
        # Insert the new record
        query = f"INSERT INTO {table_name} (content) VALUES (?)"
        self.cursor.execute(query, (content,))
        self.conn.commit()

        # Enforce the 16-row limit
        self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = self.cursor.fetchone()[0]

        if row_count > 16:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE id = (SELECT MIN(id) FROM {table_name})")
            self.conn.commit()

    def fetch_all(self, table_name):
        """Retrieve all content records from the table."""
        self.cursor.execute(f"SELECT content FROM {table_name} ORDER BY timestamp DESC")
        return [row[0] for row in self.cursor.fetchall()]  # Return a list of contents

    def clear_table(self, table_name):
        """Delete all records from the specified table."""
        self.cursor.execute(f"DELETE FROM {table_name}")
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()
