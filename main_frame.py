import json
from tkinter import ttk, messagebox, Toplevel
from utils import encrypt, embed_to_image
import tkinter as tk

class MainFrame:
    # Hapus parameter is_master_password_edit karena tidak lagi diperlukan di sini
    def __init__(self, root, theme, image_path, password, data):
        self.root = root
        self.theme = theme
        self.image_path = image_path
        self.password = password # Ini adalah password master yang sedang digunakan
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
        # Tambahkan tombol untuk mengubah master password di MainFrame
        ttk.Button(btn_frame, text="Ubah Master Password", command=self._master_password_edit_dialog).pack(side='left', padx=5)
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
            # Menampilkan password dengan asterisks
            display_password = '*' * len(e['password']) if e['password'] else ''
            ttk.Label(row, text=f"{e['app']} | {e['email']} | {display_password}", width=60, anchor='w').pack(side='left', padx=5)
            b_frame = ttk.Frame(row)
            b_frame.pack(side='right')
            ttk.Button(b_frame, text="Edit", command=lambda i=i: self._edit_entry_dialog(i), width=6).pack(side='left', padx=2)
            ttk.Button(b_frame, text="Hapus", command=lambda i=i: self._delete_entry(i), width=6).pack(side='left', padx=2)
            # Tambahkan tombol "Lihat" untuk menampilkan password asli
            ttk.Button(b_frame, text="Lihat", command=lambda p=e['password']: messagebox.showinfo("Password", p), width=6).pack(side='left', padx=2)


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
        is_error = embed_to_image(self.image_path, encrypt(json.dumps(self.data).encode('utf-8'), self.password))

        if is_error:
            messagebox.showerror("Gagal", "Gagal menyimpan data ke gambar. Pastikan gambar tidak rusak atau formatnya benar.")
        else:    
            messagebox.showinfo("Berhasil", f"Data berhasil disimpan di: {self.image_path}")

    def _logout(self):
        from gui.login_frame import LoginFrame
        LoginFrame(self.root, self.theme)

    # --- FITUR EDIT MASTER PASSWORD (dipindahkan ke MainFrame) ---
    def _master_password_edit_dialog(self):
        # Buat jendela dialog master password
        self.master_pass_dialog = Toplevel(self.root)
        self.master_pass_dialog.title("Ubah Master Password")
        self.master_pass_dialog.configure(bg=self.theme.primary)
        self.master_pass_dialog.grab_set() # Nonaktifkan interaksi dengan jendela utama sementara dialog terbuka

        frame = ttk.Frame(self.master_pass_dialog)
        frame.pack(padx=20, pady=20)

        # Labels dan Entries
        ttk.Label(frame, text="Password Master Lama:").pack(pady=5)
        self.old_pass_entry = tk.Entry(frame, show="*", fg="black", bg="white", font=self.theme.font)
        self.old_pass_entry.pack(pady=5)

        ttk.Label(frame, text="Password Master Baru:").pack(pady=5)
        self.new_pass_entry = tk.Entry(frame, show="*", fg="black", bg="white", font=self.theme.font)
        self.new_pass_entry.pack(pady=5)

        ttk.Label(frame, text="Konfirmasi Password Baru:").pack(pady=5)
        self.confirm_pass_entry = tk.Entry(frame, show="*", fg="black", bg="white", font=self.theme.font)
        self.confirm_pass_entry.pack(pady=5)

        ttk.Button(frame, text="Simpan Password Master Baru", command=self._save_new_master_password).pack(pady=15)
        
        # Menangani penutupan window edit master password
        self.master_pass_dialog.protocol("WM_DELETE_WINDOW", self._handle_master_password_dialog_close)
        
        # Tunggu sampai dialog ditutup
        self.root.wait_window(self.master_pass_dialog)

    def _save_new_master_password(self):
        old_password = self.old_pass_entry.get()
        new_password = self.new_pass_entry.get()
        confirm_password = self.confirm_pass_entry.get()

        # Validasi password lama
        if old_password != self.password:
            messagebox.showerror("Error", "Password master lama tidak cocok.", parent=self.master_pass_dialog)
            return

        # Validasi password baru
        if not new_password or not confirm_password:
            messagebox.showerror("Error", "Password baru dan konfirmasi tidak boleh kosong.", parent=self.master_pass_dialog)
            return
        if new_password != confirm_password:
            messagebox.showerror("Error", "Password baru dan konfirmasi tidak cocok.", parent=self.master_pass_dialog)
            return
        if new_password == old_password: # Cek jika password baru sama dengan password lama
             messagebox.showinfo("Informasi", "Password master baru sama dengan yang lama. Tidak ada perubahan yang disimpan.", parent=self.master_pass_dialog)
             self._handle_master_password_dialog_close() # Tutup dialog dan logout
             return

        # Enkripsi ulang data dengan password master yang baru
        encrypted_data = encrypt(json.dumps(self.data).encode('utf-8'), new_password)
        is_error = embed_to_image(self.image_path, encrypted_data)

        if is_error:
            messagebox.showerror("Gagal", "Gagal menyimpan data ke gambar dengan password baru. Pastikan gambar tidak rusak.", parent=self.master_pass_dialog)
        else:
            messagebox.showinfo("Berhasil", "Password master berhasil diubah dan data berhasil disimpan.", parent=self.master_pass_dialog)
            self.password = new_password # Update password master di instance MainFrame
            self._handle_master_password_dialog_close() # Tutup dialog dan logout

    def _handle_master_password_dialog_close(self):
        # Lepaskan "grab" dari jendela dialog
        if self.master_pass_dialog.winfo_exists(): # Cek apakah dialog masih ada
            self.master_pass_dialog.grab_release()
            self.master_pass_dialog.destroy()
        
        # Selalu kembali ke layar login setelah dialog master password ditutup
        # Ini penting agar aplikasi menggunakan password baru untuk login selanjutnya
        self._logout()
        # Tidak perlu messagebox info "dibatalkan" jika kita selalu logout