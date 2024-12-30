import ttkbootstrap as ttk
import sqlite3
from ttkbootstrap.constants import *
from peminjaman_buku import buku_dipinjam
class StatusPeminjaman:
  def __init__(self, parent):
    self.parent = parent
    self.window = ttk.Toplevel(self.parent)
    self.window.title("Status Peminjaman")
    self.window.geometry("500x550")
    self.conn = sqlite3.connect("perpus.db")
    self.cursor = self.conn.cursor()
    self.buku_dipinjam = buku_dipinjam
    self.setup_ui()
    
  def setup_ui(self):
    ttk.Label(self.window, text="Status Peminjaman", font=("Arial", 24)).pack(pady=5)
    ttk.Label(self.window, text="Judul Buku:").pack(pady=5)
    if not self.buku_dipinjam:
      ttk.Label(self.window, text="Tidak ada buku dipinjam.").pack(pady=5)
      ttk.Button(self.window, text="Kembali", bootstyle=SUCCESS, command=self.window.destroy).pack(pady=10)
      self.window.mainloop()
    else:
      self.buku_dipinjam = ", ".join(self.buku_dipinjam)
      ttk.Label(self.window, text=f"{self.buku_dipinjam}").pack(pady=5)
    self.window.mainloop()
  
  
    