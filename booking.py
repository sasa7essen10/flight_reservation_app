import tkinter as tk
from tkinter import ttk, messagebox
from database import add_reservation

class BookingPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = ttk.Label(self, text="Book a New Flight", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=20)

        labels = ["Name", "Flight Number", "Departure", "Destination", "Date", "Seat Number"]
        self.entries = {}

        for i, label in enumerate(labels):
            lbl = ttk.Label(self, text=label + ":")
            lbl.grid(row=i+1, column=0, sticky="e", padx=10, pady=5)

            entry = ttk.Entry(self, width=40)
            entry.grid(row=i+1, column=1, padx=10, pady=5)
            self.entries[label] = entry

        btn_submit = ttk.Button(self, text="Confirm Booking", command=self.save_reservation)
        btn_submit.grid(row=8, column=0, columnspan=2, pady=20)

        btn_back = ttk.Button(self, text="Back", command=lambda: controller.show_frame("HomePage"))
        btn_back.grid(row=9, column=0, columnspan=2, pady=5)

    def save_reservation(self):
        name = self.entries["Name"].get()
        flight_number = self.entries["Flight Number"].get()
        departure = self.entries["Departure"].get()
        destination = self.entries["Destination"].get()
        date = self.entries["Date"].get()
        seat_number = self.entries["Seat Number"].get()

        if not all([name, flight_number, departure, destination, date, seat_number]):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            add_reservation(name, flight_number, departure, destination, date, seat_number)
            messagebox.showinfo("Success", "Reservation added successfully!")
            for entry in self.entries.values():
                entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save reservation: {e}")
