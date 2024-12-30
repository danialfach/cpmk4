import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
from datetime import datetime
from ttkbootstrap.toast import ToastNotification
from peminjaman_buku import buku_dipinjam

class PengembalianBuku:
    def __init__(self, parent):
        self.parent = parent
        self.window = ttk.Toplevel(self.parent)
        self.window.title("Pengembalian Buku")
        self.window.geometry("500x550")
        self.conn = sqlite3.connect("perpus.db")
        self.cursor = self.conn.cursor()
        self.setup_ui()

    def kembalikan_buku(self):
        judul_buku = self.combobox_buku.get()

        if not judul_buku:
            self.label_status.config(text="Pilih buku yang akan dikembalikan", bootstyle="warning")
            return

        try:
            self.cursor.execute("UPDATE buku SET stok = stok + 1 WHERE judul = ?", (judul_buku,))
            self.cursor.execute("""
                UPDATE riwayat_peminjaman 
                SET tanggal_kembali = CURRENT_TIMESTAMP, status = 'dikembalikan'
                WHERE judul_buku = ? AND status = 'dipinjam'
            """, (judul_buku,))
            
            if judul_buku in buku_dipinjam:
                buku_dipinjam.remove(judul_buku)
                
            self.conn.commit()
            self.label_status.config(text=f"Buku berhasil dikembalikan", bootstyle="success")
            
            toast = ToastNotification(
                title="Pengembalian Berhasil",
                message=f"Buku '{judul_buku}' telah dikembalikan",
                duration=3000,
                bootstyle="success",
                position="top-center",
            )
            toast.show_toast()
            self.update_combobox()

        except sqlite3.Error as e:
            self.label_status.config(text=f"Database error: {e}", bootstyle="danger")

    def setup_ui(self):
        ttk.Label(self.window, text="Pengembalian Buku", font=("Arial", 24)).pack(pady=20)
        ttk.Label(self.window, text="Pilih buku:", font=("Arial", 12)).pack(pady=10)
        
        self.combobox_buku = ttk.Combobox(self.window, values=buku_dipinjam, width=30, state="readonly")
        self.combobox_buku.pack(pady=10)

        self.label_status = ttk.Label(self.window, text="", font=("Arial", 10))
        self.label_status.pack(pady=10)

        self.btn_kembalikan = ttk.Button(self.window, text="Kembalikan", 
                                       bootstyle="success", command=self.kembalikan_buku, width=20)
        self.btn_kembalikan.pack(pady=10)
        
        self.update_combobox()

    def update_combobox(self):
        self.combobox_buku['values'] = buku_dipinjam
        if not buku_dipinjam:
            self.label_status.config(text="Tidak ada buku dipinjam", bootstyle="warning")
            self.combobox_buku.set('')
            self.btn_kembalikan.configure(state="disabled")
        else:
            self.btn_kembalikan.configure(state="normal")

    def __del__(self):
        if self.conn:
            self.conn.close()