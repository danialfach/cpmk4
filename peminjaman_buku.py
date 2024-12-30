import ttkbootstrap as ttk
import sqlite3
from ttkbootstrap.constants import *
from datetime import datetime

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
        self.create_history_table()

    def create_history_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS riwayat_peminjaman (
                id_peminjaman INTEGER PRIMARY KEY AUTOINCREMENT,
                id_anggota INTEGER,
                judul_buku VARCHAR(255),
                tanggal_pinjam DATETIME DEFAULT CURRENT_TIMESTAMP,
                tanggal_kembali DATETIME,
                status VARCHAR(20) DEFAULT 'dipinjam',
                FOREIGN KEY (id_anggota) REFERENCES anggota(id_anggota)
            )
        """)
        self.conn.commit()

    def pinjam_buku(self):
        judul_buku = self.entry_judul_buku.get()
        nama = self.entry_nama.get()

        try:
            self.cursor.execute("SELECT id_anggota FROM anggota WHERE nama = ?", (nama,))
            member = self.cursor.fetchone()
            
            if not member:
                ttk.Label(self.window, text="Anggota tidak ditemukan.", bootstyle=DANGER).pack(pady=5)
                return

            self.cursor.execute("SELECT stok FROM buku WHERE judul = ?", (judul_buku,))
            result = self.cursor.fetchone()

            if result is None:
                ttk.Label(self.window, text="Buku tidak ditemukan.", bootstyle=DANGER).pack(pady=5)
            elif result[0] <= 0:
                ttk.Label(self.window, text="Stok buku habis.", bootstyle=WARNING).pack(pady=5)
            else:
                self.cursor.execute("UPDATE buku SET stok = stok - 1 WHERE judul = ?", (judul_buku,))
                self.cursor.execute("""
                    INSERT INTO riwayat_peminjaman (id_anggota, judul_buku)
                    VALUES (?, ?)
                """, (member[0], judul_buku))
                buku_dipinjam.append(judul_buku)
                self.conn.commit()
                ttk.Label(self.window, text=f"Peminjaman berhasil.", bootstyle=SUCCESS).pack(pady=5)
        except sqlite3.Error as e:
            ttk.Label(self.window, text=f"Database error: {e}", bootstyle=DANGER).pack(pady=5)

    def setup_ui(self):
        ttk.Label(self.window, text="Peminjaman Buku", font=("Arial", 24)).pack(pady=5)
        ttk.Label(self.window, text="Nama:").pack(pady=5)
        self.entry_nama = ttk.Entry(self.window, width=30)
        self.entry_nama.pack(pady=5)
        ttk.Label(self.window, text="Judul Buku:").pack(pady=5)
        self.entry_judul_buku = ttk.Entry(self.window, width=30)
        self.entry_judul_buku.pack(pady=5)
        ttk.Button(self.window, text="Pinjam Buku", bootstyle=SUCCESS, command=self.pinjam_buku).pack(pady=10)

    def __del__(self):
        if self.conn:
            self.conn.close()