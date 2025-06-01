import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from gui.main_frame import MainFrame
from utils import decrypt, extract_from_image

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
        ttk.Button(frame, text="Login", command=self._login).pack(fill='x', pady=20)

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
                self.data = json.loads(decrypted)
            else:
                messagebox.showerror("Error", "Password salah atau gambar rusak.")
                return
        else:
            self.data = []
        MainFrame(self.root, self.theme, self.image_path, password, self.data)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()
