import tkinter as tk
from gui.login_frame import LoginFrame
from theme import ModernTheme

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Stego Password Manager")
    root.geometry("650x450")
    root.resizable(False, False)
    theme = ModernTheme()
    app = LoginFrame(root, theme)
    root.mainloop()
