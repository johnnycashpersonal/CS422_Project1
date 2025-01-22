import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class EasyAApp:
    def __init__(self, root):
        # Set up the main application window
        self.root = root
        self.root.title("EasyA - Grade Visualizer")
        self.root.geometry("900x600")
        self.root.configure(bg="#F0F4F8")  # Light blue-gray background for a smooth feel

        # Configure button styles
        self.style = ttk.Style()
        self.style.configure(
            "TButton",
            font=("Helvetica", 12, "bold"),
            padding=6,
            foreground="#1A3C40",  # Deep teal for text
            background="#C4E3E6",  # Muted teal for background
        )
        self.style.map(
            "TButton",
            foreground=[("active", "#FFFFFF")],
            background=[("active", "#1A7B7F")],  # Brighter teal on hover
        )

        # Create each section of the app
        self.create_header()       # Input and control section at the top
        self.create_main_area()    # The central area where graphs will be displayed
        self.create_side_panel()   # Filters and options for customizing graph display
        self.create_footer()       # Status bar at the bottom

    def create_header(self):
        # Create the top section for user input and primary actions
        header_frame = tk.Frame(self.root, bg="#D5E9EB", height=60)  # Soft teal background
        header_frame.pack(fill="x")  # Stretch across the top

        # Add input fields for department, class, and year
        tk.Label(header_frame, text="Department:", bg="#D5E9EB", fg="#1A3C40", font=("Helvetica", 12)).pack(side="left", padx=10, pady=10)
        self.department_entry = ttk.Entry(header_frame, width=20)
        self.department_entry.pack(side="left", padx=5)

        tk.Label(header_frame, text="Class Number:", bg="#D5E9EB", fg="#1A3C40", font=("Helvetica", 12)).pack(side="left", padx=10, pady=10)
        self.class_entry = ttk.Entry(header_frame, width=10)
        self.class_entry.pack(side="left", padx=5)

        tk.Label(header_frame, text="Year:", bg="#D5E9EB", fg="#1A3C40", font=("Helvetica", 12)).pack(side="left", padx=10, pady=10)
        self.year_entry = ttk.Entry(header_frame, width=8)
        self.year_entry.pack(side="left", padx=5)

        # Add buttons for searching and toggling admin mode
        self.search_button = ttk.Button(header_frame, text="Search", command=self.handle_search, style="TButton")
        self.search_button.pack(side="left", padx=15)

        self.admin_button = ttk.Button(header_frame, text="Admin Mode", command=self.toggle_admin_mode, style="TButton")
        self.admin_button.pack(side="left", padx=15)

    def create_main_area(self):
        # Create the central area for displaying graphs
        self.graph_area = tk.Frame(self.root, bg="#FFFFFF", relief="ridge", bd=1)  # White background for contrast
        self.graph_area.pack(fill="both", expand=True, padx=20, pady=20)

        # Add a placeholder for the graph canvas
        self.graph_canvas = None  # To store the matplotlib canvas

    def create_side_panel(self):
        # Create a side panel for graph customization and filtering options
        side_panel = tk.Frame(self.root, bg="#C4E3E6", width=250, relief="ridge", bd=1)  # Muted teal background
        side_panel.pack(side="right", fill="y")

        # Add a title for the side panel
        tk.Label(side_panel, text="Filters", bg="#C4E3E6", fg="#1A3C40", font=("Helvetica", 14, "bold")).pack(pady=15)

        # Dropdown for selecting the X-axis
        self.x_axis_var = tk.StringVar()
        ttk.Label(side_panel, text="X-Axis:", background="#C4E3E6").pack(pady=5)
        x_axis_menu = ttk.Combobox(side_panel, textvariable=self.x_axis_var, values=["Professors", "Classes"], state="readonly")
        x_axis_menu.pack(pady=5)

        # Dropdown for selecting the Y-axis
        self.y_axis_var = tk.StringVar()
        ttk.Label(side_panel, text="Y-Axis:", background="#C4E3E6").pack(pady=5)
        y_axis_menu = ttk.Combobox(side_panel, textvariable=self.y_axis_var, values=["% As", "% Ds/Fs"], state="readonly")
        y_axis_menu.pack(pady=5)

        # Checkboxes for additional filters
        self.include_faculty_var = tk.BooleanVar()
        ttk.Checkbutton(side_panel, text="Include All Faculty", variable=self.include_faculty_var).pack(pady=10)

        self.include_class_count_var = tk.BooleanVar()
        ttk.Checkbutton(side_panel, text="Include Class Count", variable=self.include_class_count_var).pack(pady=10)

        # Button for holding the current graph on the screen
        self.hold_graph_button = ttk.Button(side_panel, text="Show Test Graph", command=self.display_test_graph, style="TButton")
        self.hold_graph_button.pack(pady=15)

    def create_footer(self):
        # Create a status bar at the bottom of the window
        footer = tk.Frame(self.root, bg="#D5E9EB", height=40)  # Soft teal background
        footer.pack(fill="x")

        # Add a status label to display messages to the user
        self.status_label = tk.Label(footer, text="Status: Ready", bg="#D5E9EB", fg="#1A3C40", font=("Helvetica", 10))
        self.status_label.pack(side="left", padx=10)

    def handle_search(self):
        # Placeholder function for search functionality
        messagebox.showinfo("Search", "Search functionality will be implemented.")

    def toggle_admin_mode(self):
        # Placeholder function for toggling admin mode
        messagebox.showinfo("Admin Mode", "Admin mode toggled.")

    def display_test_graph(self):
        # Generate a test bar chart
        data = {"Prof. A": 80, "Prof. B": 90, "Prof. C": 70, "Prof. D": 85}

        if self.graph_canvas:
            # Clear previous graph if it exists
            self.graph_canvas.get_tk_widget().destroy()

        # Create a figure for the graph
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(data.keys(), data.values(), color="#1A7B7F")  # Bar chart with teal color
        ax.set_title("Test Graph - Grade Distribution", fontsize=14)
        ax.set_ylabel("% Grades", fontsize=12)
        ax.set_xlabel("Professors", fontsize=12)

        # Embed the graph in the Tkinter canvas
        self.graph_canvas = FigureCanvasTkAgg(fig, master=self.graph_area)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Update status
        self.status_label.config(text="Status: Test graph displayed.")

    def hold_graph(self):
        # Placeholder function for holding the current graph
        messagebox.showinfo("Hold Graph", "Graph held.")


if __name__ == "__main__":
    # Launch the application
    root = tk.Tk()
    app = EasyAApp(root)
    root.mainloop()
