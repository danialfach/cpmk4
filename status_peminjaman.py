import ttkbootstrap as ttk
import sqlite3
from ttkbootstrap.constants import *
from peminjaman_buku import buku_dipinjam

class StatusPeminjaman:
    def __init__(self, parent):
        self.parent = parent
        self.window = ttk.Toplevel(self.parent)
        self.window.title("Status Peminjaman")
        self.window.iconbitmap("./img/book.ico")
        self.window.geometry("600x400")
        self.conn = sqlite3.connect("perpus.db")
        self.cursor = self.conn.cursor()
        self.buku_dipinjam = buku_dipinjam  # Local variable for tracking borrowed books
        self.setup_ui()

    def setup_ui(self):
        """Setup the UI for displaying borrowed book statuses."""
        ttk.Label(self.window, text="Status Peminjaman", font=("Arial", 24), anchor="center").pack(pady=10)

        # Create Treeview for displaying data
        columns = ("judul", "status")
        tree = ttk.Treeview(self.window, columns=columns, show="headings", bootstyle=INFO)
        tree.heading("judul", text="Judul Buku")
        tree.heading("status", text="Status")
        tree.column("judul", width=300, anchor="w")
        tree.column("status", width=150, anchor="center")
        tree.pack(pady=10, fill="both", expand=True)

        try:
            # Fetch borrowed books from the database
            self.cursor.execute("""
                SELECT buku.judul, peminjaman.status 
                FROM buku 
                JOIN peminjaman ON buku.judul = peminjaman.judul_buku
            """)
            borrowed_books = self.cursor.fetchall()

            if not borrowed_books:
                ttk.Label(self.window, text="Tidak ada buku dipinjam.", bootstyle=WARNING).pack(pady=5)
            else:
                # Insert data into Treeview
                for book in borrowed_books:
                    tree.insert("", "end", values=book)

        except sqlite3.Error as e:
            ttk.Label(self.window, text=f"Database error: {e}", bootstyle=DANGER).pack(pady=5)

        # Add a "Kembali" button
        ttk.Button(self.window, text="Kembali", bootstyle=SUCCESS, command=self.window.destroy).pack(pady=10)

    def __del__(self):
        """Ensure the database connection is closed when the object is deleted."""
        if self.conn:
            self.conn.close()
