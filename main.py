import tkinter as tk
from tkinter import ttk
from database import init_db
from home import HomePage
from booking import BookingPage
from reservations import ReservationsPage
from edit_reservation import EditReservationPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Flight Reservation")
        self.geometry("900x550")
        self.minsize(820, 480)

        # Shared data dictionary (e.g., selected_id)
        self.app_data = {}

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Page in (HomePage, BookingPage, ReservationsPage, EditReservationPage):
            frame = Page(parent=container, controller=self)
            self.frames[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        # Call on_show if it exists (useful for Edit page preload)
        if hasattr(frame, "on_show"):
            frame.on_show()

if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()
