import tkinter as tk
from tkinter import ttk, messagebox
from database import get_all_reservations, delete_reservation

class ReservationsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(2, weight=1)  # table grows
        self.grid_rowconfigure(3, weight=0)  # buttons stay bottom
        self.grid_columnconfigure(0, weight=1)

        title = ttk.Label(self, text="Reservations List", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, pady=10)

        # Search bar
        search_frame = ttk.Frame(self)
        search_frame.grid(row=1, column=0, sticky="ew", pady=5)
        self.grid_columnconfigure(0, weight=1)
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.on_show())

        # Treeview (table)
        columns = ("ID", "Name", "Flight", "Departure", "Destination", "Date", "Seat")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        y_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scroll.set)

        self.tree.grid(row=2, column=0, sticky="nsew", pady=10)
        y_scroll.grid(row=2, column=1, sticky="ns")

        # Buttons pinned to bottom
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15, sticky="s")

        btn_edit = ttk.Button(btn_frame, text="Edit Selected", command=self.edit_selected)
        btn_edit.pack(side="left", padx=10)

        btn_delete = ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected)
        btn_delete.pack(side="left", padx=10)

        btn_back = ttk.Button(btn_frame, text="Back", command=lambda: controller.show_frame("HomePage"))
        btn_back.pack(side="left", padx=10)

        # Striped rows style
        style = ttk.Style(self)
        style.configure("Treeview", rowheight=28)
        style.map("Treeview", background=[("selected", "#004080")], foreground=[("selected", "white")])
        self.tree.tag_configure("oddrow", background="#f2f2f2")
        self.tree.tag_configure("evenrow", background="white")

    def on_show(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        reservations = get_all_reservations()
        query = self.search_var.get().strip().lower()
        if query:
            reservations = [r for r in reservations if any(query in str(field).lower() for field in r)]

        for index, res in enumerate(reservations):
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            self.tree.insert("", "end", values=res, tags=(tag,))

    def get_selected_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reservation first.")
            return None
        res_id = self.tree.item(selected[0])["values"][0]
        return res_id

    def edit_selected(self):
        res_id = self.get_selected_id()
        if res_id:
            self.controller.app_data["selected_id"] = res_id
            self.controller.show_frame("EditReservationPage")

    def delete_selected(self):
        res_id = self.get_selected_id()
        if res_id:
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this reservation?")
            if confirm:
                deleted = delete_reservation(res_id)
                if deleted:
                    messagebox.showinfo("Deleted", "Reservation deleted successfully.")
                    self.on_show()
                else:
                    messagebox.showerror("Error", "Failed to delete reservation.")
