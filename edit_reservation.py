import tkinter as tk
from tkinter import ttk, messagebox
from database import get_reservation_by_id, update_reservation

class EditReservationPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = ttk.Label(self, text="Edit Reservation", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=20)

        # Form fields
        labels = ["Name", "Flight Number", "Departure", "Destination", "Date", "Seat Number"]
        self.entries = {}

        for i, label in enumerate(labels):
            lbl = ttk.Label(self, text=label + ":")
            lbl.grid(row=i+1, column=0, sticky="e", padx=10, pady=5)

            entry = ttk.Entry(self, width=40)
            entry.grid(row=i+1, column=1, padx=10, pady=5)
            self.entries[label] = entry

        # Save button
        btn_save = ttk.Button(self, text="Save Changes", command=self.save_changes)
        btn_save.grid(row=8, column=0, columnspan=2, pady=20)

        # Back button
        btn_back = ttk.Button(self, text="Back", command=lambda: controller.show_frame("ReservationsPage"))
        btn_back.grid(row=9, column=0, columnspan=2, pady=5)

    def on_show(self):
        """Load the selected reservation into the form"""
        res_id = self.controller.app_data.get("selected_id")
        if not res_id:
            messagebox.showwarning("Warning", "No reservation selected.")
            self.controller.show_frame("ReservationsPage")
            return

        reservation = get_reservation_by_id(res_id)
        if not reservation:
            messagebox.showerror("Error", "Reservation not found.")
            self.controller.show_frame("ReservationsPage")
            return

        # reservation = (id, name, flight_number, departure, destination, date, seat_number)
        _, name, flight_number, departure, destination, date, seat_number = reservation

        self.entries["Name"].delete(0, tk.END)
        self.entries["Name"].insert(0, name)

        self.entries["Flight Number"].delete(0, tk.END)
        self.entries["Flight Number"].insert(0, flight_number)

        self.entries["Departure"].delete(0, tk.END)
        self.entries["Departure"].insert(0, departure)

        self.entries["Destination"].delete(0, tk.END)
        self.entries["Destination"].insert(0, destination)

        self.entries["Date"].delete(0, tk.END)
        self.entries["Date"].insert(0, date)

        self.entries["Seat Number"].delete(0, tk.END)
        self.entries["Seat Number"].insert(0, seat_number)

    def save_changes(self):
        res_id = self.controller.app_data.get("selected_id")
        if not res_id:
            return

        name = self.entries["Name"].get()
        flight_number = self.entries["Flight Number"].get()
        departure = self.entries["Departure"].get()
        destination = self.entries["Destination"].get()
        date = self.entries["Date"].get()
        seat_number = self.entries["Seat Number"].get()

        if not all([name, flight_number, departure, destination, date, seat_number]):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        updated = update_reservation(res_id, name, flight_number, departure, destination, date, seat_number)
        if updated:
            messagebox.showinfo("Success", "Reservation updated successfully!")
            self.controller.show_frame("ReservationsPage")
        else:
            messagebox.showerror("Error", "Failed to update reservation.")
