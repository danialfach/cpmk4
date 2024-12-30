import ttkbootstrap as ttk
import sqlite3
from ttkbootstrap.constants import *

buku_dipinjam = []
class PeminjamanBuku:
    def __init__(self, parent):
        self.parent = parent
        self.window = ttk.Toplevel(self.parent)
        self.window.title("Peminjaman Buku")
        self.window.geometry("500x550")
        self.conn = sqlite3.connect("perpus.db")
        self.cursor = self.conn.cursor()
        self.setup_ui()

    def pinjam_buku(self):
        """Handle the book borrowing process and update stock."""
        judul_buku = self.entry_judul_buku.get()

        try:
            # Check if the book exists and has sufficient stock
            self.cursor.execute("SELECT stok FROM buku WHERE judul = ?", (judul_buku,))
            result = self.cursor.fetchone()

            if result is None:
                ttk.Label(self.window, text="Buku tidak ditemukan.", font=("Arial", 12), bootstyle=DANGER).pack(pady=5)
            elif result[0] <= 0:
                ttk.Label(self.window, text="Stok buku habis.", font=("Arial", 12), bootstyle=WARNING).pack(pady=5)
            else:
                # Decrease the stock by 1
                self.cursor.execute("UPDATE buku SET stok = stok - 1 WHERE judul = ?", (judul_buku,))
                buku_dipinjam.append(judul_buku)
                self.conn.commit()
                ttk.Label(self.window, text=f"Peminjaman Buku: '{judul_buku}' berhasil.", font=("Arial", 12), bootstyle=SUCCESS).pack(pady=5)
        except sqlite3.Error as e:
            ttk.Label(self.window, text=f"Database error: {e}", font=("Arial", 12), bootstyle=DANGER).pack(pady=5)

    def setup_ui(self):
        """Setup the user interface."""
        ttk.Label(self.window, text="Peminjaman Buku", font=("Arial", 24)).pack(pady=5)

        ttk.Label(self.window, text="Nama:").pack(pady=5)
        self.entry_nama = ttk.Entry(self.window, width=30)
        self.entry_nama.pack(pady=5)

        ttk.Label(self.window, text="Judul Buku:").pack(pady=5)
        self.entry_judul_buku = ttk.Entry(self.window, width=30)
        self.entry_judul_buku.pack(pady=5)

        ttk.Button(self.window, text="Pinjam Buku", bootstyle=SUCCESS, command=self.pinjam_buku).pack(pady=10)

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Ensure connection is closed when the object is deleted."""
        self.close_connection()
