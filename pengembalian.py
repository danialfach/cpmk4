import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
from ttkbootstrap.toast import ToastNotification

class PengembalianBuku:
    def __init__(self, parent):
        self.parent = parent
        self.window = ttk.Toplevel(self.parent)
        self.window.title("Pengembalian Buku")
        self.window.iconbitmap("./img/book.ico") 
        self.window.geometry("500x550")
        self.conn = sqlite3.connect("perpus.db")
        self.cursor = self.conn.cursor()
        self.setup_ui()

    def kembalikan_buku(self):
        """Handle book return process."""
        judul_buku = self.combobox_buku.get()

        if not judul_buku:
            self.label_status.config(text="Pilih buku yang akan dikembalikan", bootstyle="warning")
            return

        try:
            # Update stock and mark book as returned in the database
            self.cursor.execute("UPDATE buku SET stok = stok + 1 WHERE judul = ?", (judul_buku,))
            self.cursor.execute("UPDATE peminjaman SET status = 'dikembalikan' WHERE judul_buku = ?", (judul_buku,))
            self.conn.commit()

            # Update feedback and display a toast notification
            self.label_status.config(text=f"Buku '{judul_buku}' berhasil dikembalikan", bootstyle="success")
            toast = ToastNotification(
                title="Pengembalian Berhasil",
                message=f"Buku '{judul_buku}' telah dikembalikan",
                duration=3000,
                bootstyle="success",
                position="top-center",
            )
            toast.show_toast()

            # Refresh the combobox
            self.update_combobox()

        except sqlite3.Error as e:
            self.label_status.config(text=f"Database error: {e}", bootstyle="danger")

    def fetch_buku_dipinjam(self):
        """Fetch all currently borrowed books from the database."""
        try:
            self.cursor.execute("""
                SELECT judul_buku FROM peminjaman WHERE status = 'dipinjam'
            """)
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error fetching borrowed books: {e}")
            return []

    def setup_ui(self):
        """Setup the user interface."""
        ttk.Label(self.window, text="Pengembalian Buku", font=("Arial", 24)).pack(pady=20)
        ttk.Label(self.window, text="Pilih buku:", font=("Arial", 12)).pack(pady=10)
        
        # Combobox for selecting borrowed books
        self.combobox_buku = ttk.Combobox(self.window, values=self.fetch_buku_dipinjam(), width=30, state="readonly")
        self.combobox_buku.pack(pady=10)

        # Label for status messages
        self.label_status = ttk.Label(self.window, text="", font=("Arial", 10))
        self.label_status.pack(pady=10)

        # Button to return books
        self.btn_kembalikan = ttk.Button(
            self.window,
            text="Kembalikan",
            bootstyle="success",
            command=self.kembalikan_buku,
            width=20,
        )
        self.btn_kembalikan.pack(pady=10)
        
        # Initial combobox update
        self.update_combobox()

    def update_combobox(self):
        """Refresh the combobox with currently borrowed books."""
        buku_dipinjam = self.fetch_buku_dipinjam()
        self.combobox_buku['values'] = buku_dipinjam

        if not buku_dipinjam:
            self.label_status.config(text="Tidak ada buku dipinjam", bootstyle="warning")
            self.combobox_buku.set('')  # Clear selection
            self.btn_kembalikan.configure(state="disabled")  # Disable button if no books
        else:
            self.label_status.config(text="")  # Clear any previous warnings
            self.btn_kembalikan.configure(state="normal")

    def __del__(self):
        """Ensure the database connection is closed when the object is deleted."""
        if self.conn:
            self.conn.close()
