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
        self.window.iconbitmap("./img/book.ico")
        self.conn = sqlite3.connect("perpus.db")
        self.cursor = self.conn.cursor()
        self.setup_ui()

    def pinjam_buku(self):
        """Handle the book borrowing process."""
        judul_buku = self.entry_judul_buku.get().strip()
        nama = self.entry_nama.get().strip()

        # Clear feedback messages
        self.feedback_label.config(text="")

        try:
            # Check if anggota exists
            self.cursor.execute("SELECT id_anggota FROM anggota WHERE nama = ?", (nama,))
            member = self.cursor.fetchone()

            if not member:
                self.feedback_label.config(text="Anggota tidak ditemukan.", bootstyle=DANGER)
                return

            # Check if the book exists and has stock
            self.cursor.execute("SELECT stok FROM buku WHERE judul = ?", (judul_buku,))
            result = self.cursor.fetchone()

            if result is None:
                self.feedback_label.config(text="Buku tidak ditemukan.", bootstyle=DANGER)
            elif result[0] <= 0:
                self.feedback_label.config(text="Stok buku habis.", bootstyle=WARNING)
            else:
                # Update stock and record borrowing
                self.cursor.execute("UPDATE buku SET stok = stok - 1 WHERE judul = ?", (judul_buku,))
                self.cursor.execute("SELECT id_buku FROM buku WHERE judul = ?", (judul_buku,))
                
                self.cursor.execute("""
                    INSERT INTO peminjaman (id_anggota, judul_buku, status)
                    VALUES (?, ?, 'dipinjam')
                """, (member[0], judul_buku))
                buku_dipinjam.append(judul_buku)
                self.conn.commit()
                self.feedback_label.config(text=f"Peminjaman berhasil.", bootstyle=SUCCESS)
        except sqlite3.Error as e:
            self.feedback_label.config(text=f"Database error: {e}", bootstyle=DANGER)

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

        # Feedback Label for Messages
        self.feedback_label = ttk.Label(self.window, text="", font=("Arial", 10))
        self.feedback_label.pack(pady=5)

    def __del__(self):
        """Close the database connection when the object is deleted."""
        if self.conn:
            self.conn.close()
