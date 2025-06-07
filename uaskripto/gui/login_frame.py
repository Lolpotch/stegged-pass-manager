import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from gui.main_frame import MainFrame
from utils import decrypt, extract_from_image, encrypt, embed_to_image # Import encrypt dan embed_to_image

class LoginFrame:
    def __init__(self, root, theme):
        self.root = root
        self.theme = theme
        self.style = ttk.Style()
        self._apply_style()
        self._build_login()

    def _apply_style(self):
        self.root.configure(bg=self.theme.primary)
        self.style.theme_use('clam')
        self.style.configure('.', background=self.theme.primary, foreground=self.theme.text, font=self.theme.font)
        self.style.configure('TButton', background=self.theme.secondary, foreground=self.theme.text, padding=6)
        self.style.map('TButton', background=[('active', self.theme.accent)])

    def _build_login(self):
        self.clear_root()
        frame = ttk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(frame, text="Stego Password Manager", font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))
        ttk.Button(frame, text="Pilih Gambar", command=self._browse_image).pack(fill='x', pady=5)
        self.img_label = ttk.Label(frame, text="Belum ada gambar dipilih")
        self.img_label.pack(pady=5)

        ttk.Label(frame, text="Password Master:").pack(pady=(15, 5))
        self.pass_entry = tk.Entry(frame, show="*", fg="black", bg="white", font=self.theme.font)
        self.pass_entry.pack(fill='x', pady=5)

        ttk.Button(frame, text="Login", command=self._login).pack(fill='x', pady=10)
        # Tambahkan tombol untuk mengedit/membuat password master
        ttk.Button(frame, text="Buat/Ganti Master Password", command=self._create_or_edit_master_password).pack(fill='x', pady=5)


        self.image_path = ''
        self.data = []

    def _browse_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            self.image_path = path
            self.img_label.config(text=os.path.basename(path))

    def _login(self):
        password = self.pass_entry.get()
        if not self.image_path or not password:
            messagebox.showerror("Error", "Pilih gambar dan isi password master!")
            return
        raw = extract_from_image(self.image_path)
        if raw:
            decrypted = decrypt(raw, password)
            if decrypted:
                try:
                    self.data = json.loads(decrypted)
                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Data tersembunyi rusak atau tidak valid.")
                    return
            else:
                messagebox.showerror("Error", "Password salah atau gambar rusak.")
                return
        else:
            self.data = [] # Jika tidak ada data tersembunyi, inisialisasi sebagai list kosong
        MainFrame(self.root, self.theme, self.image_path, password, self.data)

    def _create_or_edit_master_password(self):
        if not self.image_path:
            messagebox.showerror("Error", "Pilih gambar terlebih dahulu untuk membuat atau mengganti master password.")
            return

        # Kita akan menggunakan MainFrame untuk melakukan edit setelah master password baru diinput
        # Untuk tujuan ini, kita perlu meminta password master LAMA (jika ada) atau master password BARU.
        # Karena kita belum login, kita tidak tahu password lama.
        # Pendekatan terbaik adalah meminta password master LAMA dulu,
        # mendekripsi data dengan itu, lalu meminta password master BARU.

        temp_password = self.pass_entry.get() # Ambil password yang diinput pengguna
        if not temp_password:
            messagebox.showerror("Error", "Masukkan password master yang ada (jika ada) atau password master baru yang Anda inginkan untuk gambar ini.")
            return

        raw = extract_from_image(self.image_path)
        current_data = []

        if raw: # Jika ada data tersembunyi di gambar
            decrypted_data = decrypt(raw, temp_password)
            if decrypted_data:
                try:
                    current_data = json.loads(decrypted_data)
                except json.JSONDecodeError:
                    # Ini berarti password yang dimasukkan salah, atau data rusak
                    messagebox.showerror("Gagal", "Password master yang Anda masukkan tidak cocok dengan data yang ada di gambar.")
                    return
            else:
                # Password salah atau data rusak, tapi ada data
                messagebox.showerror("Gagal", "Password master yang Anda masukkan salah atau data di gambar rusak. Tidak dapat mengedit master password.")
                return
        else:
            # Tidak ada data tersembunyi di gambar, ini adalah pembuatan master password baru
            # current_data tetap []
            pass # Lanjutkan dengan current_data = []

        # Setelah berhasil mendapatkan (atau menginisialisasi) current_data
        # Kita panggil MainFrame dengan password master yang BARU saja diinput sebagai master password baru
        # Dan data yang sudah didekripsi (atau kosong)
        # MainFrame akan menampilkan dialog untuk konfirmasi password master baru dan menyimpannya.
        MainFrame(self.root, self.theme, self.image_path, temp_password, current_data, is_master_password_edit=True)


    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()