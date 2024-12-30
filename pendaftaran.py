import ttkbootstrap as ttk
import sqlite3  
class Registration:
    def __init__(self, parent):
        self.parent = parent
        self.window = ttk.Toplevel(self.parent)  # Create a new window for registration
        self.window.title("Registration")
        self.window.iconbitmap("assets/img/book.ico")
        self.window.geometry("500x550")
        self.conn = sqlite3.connect("perpus.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        self.setup_ui()

    def create_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS anggota (
                    id_anggota INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama VARCHAR(255) NOT NULL,
                    alamat TEXT,
                    no_telpon VARCHAR(15),
                    email VARCHAR(100),
                    password VARCHAR(12)
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def register_user(self):
        nama = self.entry_nama.get()
        alamat = self.entry_alamat.get()
        no_telpon = self.entry_notelepon.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()

        if password != confirm_password:
            self.label_error.config(text="Passwords do not match!", bootstyle="danger")
        else:
            try:
                self.cursor.execute(
                    "INSERT INTO anggota (nama, alamat, no_telpon, email, password) VALUES (?, ?, ?, ?, ?)",
                    (nama, alamat, no_telpon, email, password),
                )
                self.conn.commit()
                self.entry_nama.configure(state="disabled")
                self.entry_alamat.configure(state="disabled")
                self.entry_notelepon.configure(state="disabled")
                self.entry_email.configure(state="disabled")
                self.entry_password.configure(state="disabled")
                self.entry_confirm_password.configure(state="disabled")
                self.label_error.config(text="Registration Successful!", bootstyle="success")
            except sqlite3.IntegrityError:
                self.label_error.config(text="NPM already exists!", bootstyle="danger")
            except sqlite3.Error as e:
                self.label_error.config(text=f"Database error: {e}", bootstyle="danger")

    def setup_ui(self):
        ttk.Label(self.window, text="Nama:").pack(pady=5)
        self.entry_nama = ttk.Entry(self.window, width=30)
        self.entry_nama.pack(pady=5)

        ttk.Label(self.window, text="Alamat:").pack(pady=5)
        self.entry_alamat = ttk.Entry(self.window, width=30)
        self.entry_alamat.pack(pady=5)

        ttk.Label(self.window, text="No. Telepon:").pack(pady=5)
        self.entry_notelepon = ttk.Entry(self.window, width=30)
        self.entry_notelepon.pack(pady=5)

        ttk.Label(self.window, text="Email:").pack(pady=5)
        self.entry_email = ttk.Entry(self.window, width=30)
        self.entry_email.pack(pady=5)

        ttk.Label(self.window, text="Password:").pack(pady=5)
        self.entry_password = ttk.Entry(self.window, show="*", width=30)
        self.entry_password.pack(pady=5)
        
        ttk.Label(self.window, text="Confirm Password:").pack(pady=5)
        self.entry_confirm_password = ttk.Entry(self.window, show="*", width=30)
        self.entry_confirm_password.pack(pady=5)

        self.label_error = ttk.Label(self.window, text="", bootstyle="danger")
        self.label_error.pack(pady=5)

        ttk.Button(
            self.window, text="Register", bootstyle="success", command=self.register_user
        ).pack(pady=10)