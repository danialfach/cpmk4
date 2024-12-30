import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
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
        """Handle the book return process and update stock."""
        judul_buku = self.combobox_buku.get()

        if not judul_buku:
            self.label_status.config(text="Silakan pilih buku yang akan dikembalikan", bootstyle="warning")
            return

        try:
            self.cursor.execute("UPDATE buku SET stok = stok + 1 WHERE judul = ?", (judul_buku,))
            self.conn.commit()

            if judul_buku in buku_dipinjam:
                buku_dipinjam.remove(judul_buku)

            self.label_status.config(text=f"Buku '{judul_buku}' berhasil dikembalikan", bootstyle="success")
            
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

    def update_combobox(self):
        """Update the combobox with current borrowed books."""
        self.combobox_buku['values'] = buku_dipinjam
        if not buku_dipinjam:
            self.label_status.config(text="Tidak ada buku yang dipinjam", bootstyle="warning")
            self.combobox_buku.set('')
            self.btn_kembalikan.configure(state="disabled")
        else:
            self.btn_kembalikan.configure(state="normal")

    def setup_ui(self):
        """Setup the user interface."""
        ttk.Label(
            self.window,
            text="Pengembalian Buku",
            font=("Arial", 24)
        ).pack(pady=20)

        ttk.Label(
            self.window,
            text="Pilih buku yang akan dikembalikan:",
            font=("Arial", 12)
        ).pack(pady=10)

        self.combobox_buku = ttk.Combobox(
            self.window,
            values=buku_dipinjam,
            width=30,
            state="readonly"
        )
        self.combobox_buku.pack(pady=10)

        self.label_status = ttk.Label(
            self.window,
            text="",
            font=("Arial", 10)
        )
        self.label_status.pack(pady=10)

        self.btn_kembalikan = ttk.Button(
            self.window,
            text="Kembalikan Buku",
            bootstyle="success",
            command=self.kembalikan_buku,
            width=20
        )
        self.btn_kembalikan.pack(pady=10)

        ttk.Button(
            self.window,
            text="Tutup",
            bootstyle="secondary",
            command=self.window.destroy,
            width=20
        ).pack(pady=5)

        self.update_combobox()

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Ensure connection is closed when the object is deleted."""
        self.close_connection()