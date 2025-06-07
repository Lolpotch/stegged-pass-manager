import json
from tkinter import ttk, messagebox, Toplevel
from utils import encrypt, embed_to_image

class MainFrame:
    def __init__(self, root, theme, image_path, password, data):
        self.root = root
        self.theme = theme
        self.image_path = image_path
        self.password = password
        self.data = data
        self._build_main()

    def _build_main(self):
        for w in self.root.winfo_children(): w.destroy()

        header = ttk.Frame(self.root)
        header.pack(fill='x', padx=20, pady=10)
        ttk.Label(header, text="Password Tersimpan", font=("Segoe UI", 13, "bold")).pack(side='left')

        btn_frame = ttk.Frame(header)
        btn_frame.pack(side='right')
        ttk.Button(btn_frame, text="Tambah Baru", command=self._add_entry_dialog).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Simpan ke Gambar", command=self._save_to_image).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Logout", command=self._logout).pack(side='left', padx=5)

        self.entries_frame = ttk.Frame(self.root)
        self.entries_frame.pack(fill='both', expand=True, padx=25, pady=(0, 10))
        self._display_entries()

    def _display_entries(self):
        for w in self.entries_frame.winfo_children(): w.destroy()
        if not self.data:
            ttk.Label(self.entries_frame, text="Belum ada data.").pack(pady=20)
            return
        for i, e in enumerate(self.data):
            row = ttk.Frame(self.entries_frame)
            row.pack(fill='x', pady=3)
            ttk.Label(row, text=f"{e['app']} | {e['email']} | {e['password']}", width=60, anchor='w').pack(side='left', padx=5)
            b_frame = ttk.Frame(row)
            b_frame.pack(side='right')
            ttk.Button(b_frame, text="Edit", command=lambda i=i: self._edit_entry_dialog(i), width=6).pack(side='left', padx=2)
            ttk.Button(b_frame, text="Hapus", command=lambda i=i: self._delete_entry(i), width=6).pack(side='left', padx=2)

    def _edit_entry_dialog(self, i):
        self._entry_dialog("Edit Entri", self.data[i], lambda d: self._update_entry(i, d))

    def _add_entry_dialog(self):
        self._entry_dialog("Tambah Entri", {}, self._add_entry)

    def _entry_dialog(self, title, default, callback):
        win = Toplevel(self.root)
        win.title(title)
        win.configure(bg=self.theme.primary)
        frame = ttk.Frame(win)
        frame.pack(padx=20, pady=20)

        def field(row, label, value=''):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky='w', pady=5)
            entry = ttk.Entry(frame)
            entry.insert(0, value)
            entry.grid(row=row, column=1, pady=5, padx=10)
            return entry

        e_app = field(0, "Nama Aplikasi:", default.get('app', ''))
        e_email = field(1, "Email/Username:", default.get('email', ''))
        e_pass = field(2, "Password:", default.get('password', ''))

        def save():
            callback({'app': e_app.get(), 'email': e_email.get(), 'password': e_pass.get()})
            win.destroy()

        ttk.Button(frame, text="Simpan", command=save).grid(row=3, columnspan=2, pady=15)

    def _add_entry(self, entry):
        self.data.append(entry)
        self._display_entries()

    def _update_entry(self, i, entry):
        self.data[i] = entry
        self._display_entries()

    def _delete_entry(self, i):
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus entri ini?"):
            self.data.pop(i)
            self._display_entries()

    def _save_to_image(self):
        is_error = embed_to_image(self.image_path, encrypt(json.dumps(self.data), self.password))

        if is_error:
            messagebox.showerror("Gagal", "Gagal menyimpan data ke gambar. Pastikan gambar tidak rusak atau formatnya benar.")
        else:   
            messagebox.showinfo("Berhasil", f"Data berhasil disimpan di: {self.image_path}")

    def _logout(self):
        from gui.login_frame import LoginFrame
        LoginFrame(self.root, self.theme)
