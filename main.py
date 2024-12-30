import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
from pendaftaran import Registration
from daftar_buku import DaftarBuku
from peminjaman_buku import PeminjamanBuku
from pengembalian import PengembalianBuku
from status_peminjaman import StatusPeminjaman
from ttkbootstrap.toast import ToastNotification


# Main Application
def show_page(page_to_show):
    """Switches between application pages."""
    page1.pack_forget()
    page2.pack_forget()
    page_to_show.pack(fill="both", expand=True)


def open_registration():
    """Opens the Registration window using the Registration class."""
    Registration(root)


def validate_login():
    """Validates the user's login credentials."""
    nama = entry_nama.get()
    password = entry_password.get()

    conn = sqlite3.connect("perpus.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM anggota WHERE nama = ? AND password = ?", (nama, password))
        user = cursor.fetchone()

        if user:
            label_error_login.config(text="Login Successful!", bootstyle="success")
            show_page(page2)

            # Display toast notification
            toast = ToastNotification(
                title="Login Berhasil",
                message=f"Selamat datang, {user[1]}!",
                duration=5000,
                bootstyle="success",
                position="top-center",
            )
            toast.show_toast()
        else:
            label_error_login.config(text="Invalid Username or Password", bootstyle="danger")
    except sqlite3.Error as e:
        label_error_login.config(text=f"Database error: {e}", bootstyle="danger")
    finally:
        conn.close()


# Database Setup
conn = sqlite3.connect("perpus.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS anggota (
                    id_anggota INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama VARCHAR(255) NOT NULL,
                    alamat TEXT,
                    no_telpon VARCHAR(15),
                    email VARCHAR(100),
                    password VARCHAR(12)
                )
""")
conn.close()

# Main Window
root = ttk.Window(themename="journal", size=(700, 400))
root.title("Perpustakaan Ngawi")
root.iconbitmap("./assets/img/book.ico")
root.resizable(False, False)

page1 = ttk.Frame(root)
page2 = ttk.Frame(root)

# Page 1: Login Page
ttk.Label(page1, text="Selamat Datang!", font=("Arial", 24)).pack(pady=4)
ttk.Label(page1, text="Silakan login untuk masuk ke perpustakaan").pack(pady=4)
ttk.Label(page1, text="Nama:").pack(pady=5)
entry_nama = ttk.Entry(page1)
entry_nama.pack(pady=5)
ttk.Label(page1, text="Password:").pack(pady=5)
entry_password = ttk.Entry(page1, show="*", bootstyle="info")
entry_password.pack(pady=5)

label_error_login = ttk.Label(page1, text="", bootstyle="danger")
label_error_login.pack(pady=5)

ttk.Button(page1, text="Login", bootstyle="success", command=validate_login).pack(pady=10)
ttk.Button(page1, text="Klik disini untuk mendaftar", bootstyle="info", command=open_registration).pack(pady=10)

# Page 2: Main Page
ttk.Label(page2, text="Silakan pilih menu", font=("Arial", 24)).pack(pady=20)
menu_items = [
    ("Daftar Buku", lambda: DaftarBuku(root)),
    ("Peminjaman Buku", lambda: PeminjamanBuku(root)),
    ("Pengembalian Buku", lambda: PengembalianBuku(root)),
    ("Status Peminjaman", lambda: StatusPeminjaman(root)),
]

for menu_text, command in menu_items:
    ttk.Button(page2, text=menu_text, bootstyle="success", command=command, width=20).pack(pady=10)

# Show the first page
show_page(page1)

root.mainloop()
