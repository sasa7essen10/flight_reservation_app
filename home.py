import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # When running from a PyInstaller bundle
        base_path = sys._MEIPASS
    except Exception:
        # When running from source
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # 🖼 Load Logo safely (works in .exe and normal run)
        try:
            logo_path = resource_path("logo.png")
            img = Image.open(logo_path).resize((120, 120))
            self.logo = ImageTk.PhotoImage(img)
            logo_label = ttk.Label(self, image=self.logo)
            logo_label.pack(pady=20)
        except Exception as e:
            print("⚠️ Logo not loaded:", e)

        # Title and subtitle
        title = ttk.Label(self, text="Flight Reservation System", font=("Segoe UI", 20, "bold"))
        subtitle = ttk.Label(self, text="Choose an option:", font=("Segoe UI", 12))

        title.pack(pady=(10, 5))
        subtitle.pack(pady=(0, 20))

        # Navigation buttons
        btn_book = ttk.Button(self, text="Book New Flight",
                              command=lambda: controller.show_frame("BookingPage"))
        btn_view = ttk.Button(self, text="View All Reservations",
                              command=lambda: controller.show_frame("ReservationsPage"))

        btn_book.pack(pady=8, ipadx=10, ipady=5)
        btn_view.pack(pady=8, ipadx=10, ipady=5)
