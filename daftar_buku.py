import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3

class DaftarBuku:
    def __init__(self, parent):
        self.parent = parent
        self.window = ttk.Toplevel(self.parent)  # Create a new window for Daftar Buku
        self.window.title("Daftar Buku")
        self.window.geometry("500x550")
        self.conn = sqlite3.connect("perpus.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        self.daftar_buku = self.get_books()  # Fetch books data
        self.setup_ui()

    def create_table(self):
        """Create the 'buku' table if it doesn't exist."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS buku (
                    id_buku INTEGER PRIMARY KEY AUTOINCREMENT,
                    judul VARCHAR(255) NOT NULL,
                    pengarang VARCHAR(255) NOT NULL,
                    penerbit VARCHAR(255) NOT NULL,
                    tahun_terbit INTEGER,
                    stok INTEGER NOT NULL
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def get_books(self):
        """Fetch all books from the database."""
        try:
            return self.cursor.execute("SELECT * FROM buku").fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching books: {e}")
            return []

    def setup_ui(self):
        """Setup the user interface to display the list of books."""
        ttk.Label(self.window, text="Daftar Buku", font=("Arial", 24), anchor="center").pack(pady=10)

        if not self.daftar_buku:
            ttk.Label(self.window, text="Tidak ada buku di database.", font=("Arial", 12), bootstyle="danger").pack(pady=10)
            return

        # Display each book
        for buku in self.daftar_buku:
            ttk.Label(self.window, text=f"Judul: {buku[1]}", font=("Arial", 10)).pack(anchor="w", padx=20)
            ttk.Label(self.window, text=f"Pengarang: {buku[2]}", font=("Arial", 10)).pack(anchor="w", padx=20)
            ttk.Label(self.window, text=f"Tahun Terbit: {buku[4]}", font=("Arial", 10)).pack(anchor="w", padx=20)
            ttk.Label(self.window, text=f"Stok: {buku[5]}", font=("Arial", 10)).pack(anchor="w", padx=20)
            ttk.Separator(self.window, orient="horizontal").pack(fill="x", pady=15)

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Ensure connection is closed when the object is deleted."""
        self.close_connection()
