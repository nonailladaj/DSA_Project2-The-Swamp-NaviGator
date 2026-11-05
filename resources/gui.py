import time
import tkinter as tk
from tkinter import messagebox, ttk

class SwampNaviGatorApp:

    def __init__(self, root, db_instance):
        self.root = root
        self.root.title("The Swamp NaviGator 🐊")
        self.root.geometry("700x720")
        self.root.config(bg="#f4f6f9")

        self.db = db_instance

        # App Header
        title_label = tk.Label(
            root,
            text = "The Swamp Navigator",
            font = ("Helvetica", 18, "bold"),
            bg = "#f4f6f9",
            fg = "#0021A5",
        )
        title_label.pack(pady = 10)

        subtitle_label = tk.Label(
            root,
            text = (
                "Find the best spots in Gainesville based on crowd, costs, & events!"
            ),
            font=("Helvetica", 10, "italic"),
            bg = "#f4f6f9",
            fg = "#555555",
        )
        subtitle_label.pack(pady = 2)

        # Input Frame (Dropdown Menus)
        input_frame = tk.LabelFrame(
            root,
            text = "User Preferences ",
            font=("Helvetica", 12, "bold"),
            bg="#ffffff",
            fg="#fa4616",
            bd = 2,
            relief = "groove",
        )
        input_frame.pack(fill = "x", padx=20, pady=10, ipadx=10, ipady=10)

        # 1. Location / Category Dropdown
        tk.Label(
            input_frame, text="Preferred Location / Category: ", bg = "#ffffff"
        ).grid(row = 0, column = 0, sticky = "w", padx = 10, pady = 5)
        self.location_var = tk.StringVar()
        self.location_combo = ttk.Combobox(
            input_frame,
            textvariable = self.location_var,
            values = [
                "Midtown",
                "Downtown",
            ],
            state = "readonly"
        )
        self.location_combo.grid(row = 0, column = 1, padx = 10, pady = 5)
        self.location_combo.current(0)

        # 2. Day / Event Dropdown
        tk.Label(input_frame, text = "Preferred Day / Event: ", bg = "#ffffff").grid(
            row = 1, column = 0, sticky = "w", padx = 10, pady = 5
        )
        self.day_var = tk.StringVar()
        self.day_combo = ttk.Combobox(
            input_frame,
            textvariable = self.day_var,
            values = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ] ,
            state = "readonly"
        )
        self.day_combo.grid(row = 1, column = 1, padx = 10, pady = 5)
        self.day_combo.current(5)

        # 3. Crown Level Dropdown
        tk.Label(input_frame, text = "Preferred Crowd Level: ", bg = "#ffffff").grid(
            row = 2, column = 0, sticky = "w", padx = 5, pady = 5
        )
        self.crowd_var = tk.StringVar()
        self.crowd_combo = ttk.Combobox(
            input_frame,
            textvariable = self.crowd_var,
            values = ["Low (Quiet)", "Moderate", "Packed / Lively"],
            state = "readonly"
        )
        self.crowd_combo.grid(row = 2, column = 1, padx = 10, pady = 5)
        self.crowd_combo.current(1)

        # 4. Time/ Budget Dropdown
        tk.Label(
            input_frame, text = "Preferred Time & Budget: ", bg = "#ffffff"
        ).grid(row = 3, column = 0, sticky = "w", padx = 5, pady = 5)
        self.time_var = tk.StringVar()
        self.time_combo = ttk.Combobox(
            input_frame,
            textvariable = self.time_var,
            values = [
                "Evening (6 PM - 9 PM) [$]",
                "Night (9 PM - 12 AM) [$$$]",
                "Late Night (12 AM+) [$$$]"
            ],
            state="readonly",
        )
        self.time_combo.grid(row = 3, column = 1, padx = 10, pady = 5)
        self.time_combo.current(0)

        # Search Button
        search_btn = tk.Button(
            root,
            text = "Find Top 10 Spots",
            font=("Helvetica", 11, "bold"),
            bg = "#0021A5",
            fg = "white",
            activebackground = "#f4f6f9",
            activeforeground = "white",
            command = self.execute_search,
        )
        search_btn.pack(pady = 5)

        # Output Frame (Top 10 Results)
        output_frame = tk.LabelFrame(
            root,
            text = "Top 10 Recommendations ",
            font = ("Helvetica", 12, "bold"),
            bg = "#ffffff",
            fg = "#0021A5",
            bd = 2,
            relief = "groove",
        )
        output_frame.pack(fill = "both", expand = True, padx = 20, pady = 10)

        # Scrollable Text Box for Top 10 List
        self.results_text = tk.Text(
            output_frame,
            height = 10,
            width = 75,
            font = ("Courier", 10),
            bg = "#fafafa",
            relief = "solid",
            bd = 1,
        )
        self.results_text.pack(side = "left", fill = "both", expand = True, padx = 5, pady = 5)

        scrollbar = tk.Scrollbar(
            output_frame, command = self.results_text.yview
        )
        scrollbar.pack(side = "right", fill = "y")
        self.results_text.configure(yscrollcommand = scrollbar.set)

        # Metrics Label
        self.metrics_label = tk.Label(
            root,
            text = (
                "Algorithm Performance Comparison: Run a search to see execution times."
            ),
            font = ("Helvetica", 9, "italic"),
            bg = "#f4f6f9",
            fg = "#333",
        )
        self.metrics_label.pack(pady = 5)

    def execute_search(self):
        user_prefs = {
            "location": self.location_var.get(),
            "day": self.day_var.get(),
            "crowd": self.crowd_var.get(),
            "time": self.time_var.get(),
        }

        # TODO Connect to backend here

if __name__ == "__main__":
    root = tk.Tk()
    app = SwampNaviGatorApp(root, db_instance = None)
    root.mainloop()