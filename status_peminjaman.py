import ttkbootstrap as ttk
import sqlite3
from ttkbootstrap.constants import *

class StatusPeminjaman:
    def __init__(self, parent):
        self.parent = parent
        self.window = ttk.Toplevel(self.parent)
        self.window.title("Status Peminjaman")
        self.window.iconbitmap("./img/book.ico")
        self.window.geometry("600x400")
        self.conn = sqlite3.connect("perpus.db")
        self.cursor = self.conn.cursor()
        self.setup_ui()

    def setup_ui(self):
        """Setup the UI for displaying borrowed book statuses."""
        ttk.Label(self.window, text="Status Peminjaman", font=("Arial", 24), anchor="center").pack(pady=10)

        # Create Treeview for displaying data
        columns = ("judul", "status", "stok")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", bootstyle=INFO)
        self.tree.heading("judul", text="Judul Buku")
        self.tree.heading("status", text="Status")
        self.tree.heading("stok", text="Stok")
        self.tree.column("judul", width=250, anchor="w")
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("stok", width=50, anchor="center")
        self.tree.pack(pady=10, fill="both", expand=True)

        # Populate Treeview
        self.update_treeview()

        # Add a "Kembali" button
        ttk.Button(self.window, text="Kembali", bootstyle=SUCCESS, command=self.window.destroy).pack(pady=10)

    def update_treeview(self):
        """Update the Treeview with current borrowed books."""
        # Clear the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # Fetch borrowed books with their stock
            self.cursor.execute("""
                SELECT buku.judul, peminjaman.status, buku.stok 
                FROM buku 
                JOIN peminjaman ON buku.judul = peminjaman.judul_buku
                WHERE peminjaman.status = 'dipinjam'
            """)
            borrowed_books = self.cursor.fetchall()

            if not borrowed_books:
                ttk.Label(self.window, text="Tidak ada buku dipinjam.", bootstyle=WARNING).pack(pady=5)
            else:
                # Insert data into Treeview
                for book in borrowed_books:
                    self.tree.insert("", "end", values=book)

        except sqlite3.Error as e:
            ttk.Label(self.window, text=f"Database error: {e}", bootstyle=DANGER).pack(pady=5)

    def decrease_stock(self, book_title):
        """Decrease stock for a specific book in the database and update the Treeview."""
        try:
            # Decrease stock in the database
            self.cursor.execute("SELECT stok FROM buku WHERE judul = ?", (book_title,))
            stock = self.cursor.fetchone()

            if stock and stock[0] > 0:
                new_stock = stock[0] - 1
                self.cursor.execute("UPDATE buku SET stok = ? WHERE judul = ?", (new_stock, book_title))
                self.conn.commit()

                # Update Treeview
                if new_stock <= 0:
                    for item in self.tree.get_children():
                        values = self.tree.item(item, "values")
                        if values[0] == book_title:
                            self.tree.delete(item)
                            break
                else:
                    self.update_treeview()

        except sqlite3.Error as e:
            ttk.Label(self.window, text=f"Error updating stock: {e}", bootstyle=DANGER).pack(pady=5)

    def check_and_update_stock(self):
        """Fetch and update stock for all borrowed books dynamically."""
        try:
            self.cursor.execute("""
                SELECT peminjaman.judul_buku 
                FROM peminjaman 
                JOIN buku ON peminjaman.judul_buku = buku.judul
                WHERE buku.stok <= 0 AND peminjaman.status = 'dipinjam'
            """)
            zero_stock_books = [row[0] for row in self.cursor.fetchall()]

            for book_title in zero_stock_books:
                for item in self.tree.get_children():
                    values = self.tree.item(item, "values")
                    if values[0] == book_title:
                        self.tree.delete(item)
                        break

        except sqlite3.Error as e:
            ttk.Label(self.window, text=f"Error checking stock: {e}", bootstyle=DANGER).pack(pady=5)

    def __del__(self):
        """Ensure the database connection is closed when the object is deleted."""
        if self.conn:
            self.conn.close()
