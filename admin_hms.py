"""
admin_hms.py — Doctor Login Screen
====================================
QA-14 FIX: 'previous()' no longer re-imports ZEM_HMS and re-populates
            the navigation list on every back-press.
QA-32 FIX: Admin credentials read from .env (ADMIN_USER, ADMIN_PASS_HASH).
            Falls back to built-in defaults if not set.
"""

from customtkinter import *
from PIL import Image
from tkinter import messagebox
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

# ── Credentials (QA-32 FIX: read from .env, fall back to hashed defaults) ────
# To override, add to .env:
#   ADMIN_USER=admin
#   ADMIN_PASS_HASH=<sha256 of your password>
_ADMIN_USER      = os.getenv('ADMIN_USER', 'admin')
_DEFAULT_HASH    = hashlib.sha256(b'Admin@123').hexdigest()
_ADMIN_PASS_HASH = os.getenv('ADMIN_PASS_HASH', _DEFAULT_HASH)


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def run():
    """All UI code is wrapped here — does NOT execute on import."""

    def login():
        user = userName.get().strip()
        pwd  = userPassword.get()
        if not user or not pwd:
            messagebox.showerror('Error', 'All fields are required')
        elif user == _ADMIN_USER and _hash(pwd) == _ADMIN_PASS_HASH:
            root.destroy()
            import doctor_screen
            doctor_screen.run()
        else:
            messagebox.showerror('Error', 'Wrong credentials')

    def previous():
        """
        QA-14 FIX: Instead of re-importing ZEM_HMS (which re-appends 5 nodes
        to the navigation list every single call), we call user_screen()
        directly from the already-loaded module — no re-import, no list growth.
        """
        root.destroy()
        import ZEM_HMS
        # Call user_screen directly — ZEM_HMS is already in sys.modules,
        # so no re-execution of module-level code, no list duplication.
        ZEM_HMS.navigation_list.seek("User Screen")
        ZEM_HMS.user_screen()

    root = CTk()
    root.geometry("950x450")
    root.resizable(False, False)
    root.title("Doctor Login — ZEM Hospital")

    image = CTkImage(Image.open('zem.png'), size=(950, 450))
    CTkLabel(root, image=image, text="").place(x=0, y=0)

    CTkLabel(root,
             text="Welcome to ZEM Hospital",
             fg_color="#097999",
             text_color="white",
             font=("Goudy Old Style", 30, "bold")).place(x=30, y=150)

    userName = CTkEntry(root, placeholder_text='Enter your Username')
    userName.place(x=120, y=190)

    userPassword = CTkEntry(root, placeholder_text='Enter your Password', show='*')
    userPassword.place(x=120, y=230)

    CTkButton(root, text='Login', cursor='hand2', command=login).place(x=120, y=270)
    CTkButton(root, text='Back',  cursor='hand2', command=previous).place(x=120, y=310)

    root.mainloop()


if __name__ == '__main__':
    run()