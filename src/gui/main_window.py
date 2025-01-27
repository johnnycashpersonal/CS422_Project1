import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EasyAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EasyA - Grade Visualizer")
        self.root.geometry("900x600")
        self.root.configure(bg="#FFFFFF")  # Clean white background

        # Configure global styles
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Modern look
        self.style.configure("TButton", font=("Helvetica", 12), padding=6)
        self.style.map(
            "TButton",
            foreground=[("active", "#FFFFFF")],
            background=[("active", "#4CAF50")],  # Green hover effect
        )

        self.create_header()
        self.create_main_area()
        self.create_side_panel()
        self.create_footer()

    def create_header(self):
        header = tk.Frame(self.root, bg="#F5F5F5", height=60, pady=10)
        header.pack(fill="x")

        tk.Label(header, text="Department:", bg="#F5F5F5", fg="#000000", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
        self.department_entry = ttk.Entry(header, width=15)
        self.department_entry.grid(row=0, column=1, padx=5)

        tk.Label(header, text="Class Number:", bg="#F5F5F5", fg="#000000", font=("Helvetica", 12)).grid(row=0, column=2, padx=5)
        self.class_entry = ttk.Entry(header, width=10)
        self.class_entry.grid(row=0, column=3, padx=5)

        tk.Label(header, text="Year:", bg="#F5F5F5", fg="#000000", font=("Helvetica", 12)).grid(row=0, column=4, padx=5)
        self.year_entry = ttk.Entry(header, width=8)
        self.year_entry.grid(row=0, column=5, padx=5)

        ttk.Button(header, text="Search", command=self.handle_search).grid(row=0, column=6, padx=15)
        ttk.Button(header, text="Admin Mode", command=self.toggle_admin_mode).grid(row=0, column=7, padx=15)


    def create_main_area(self):
        self.graph_area = tk.Frame(self.root, bg="#FFFFFF", relief="ridge", bd=2)
        self.graph_area.pack(fill="both", expand=True, padx=20, pady=20)

        self.graph_canvas = None

    def create_side_panel(self):
        side_panel = tk.Frame(self.root, bg="#F5F5F5", width=250, relief="ridge", bd=2)
        side_panel.pack(side="right", fill="y")

        tk.Label(side_panel, text="Filters", bg="#F5F5F5", font=("Helvetica", 14, "bold")).pack(pady=15)

        ttk.Label(side_panel, text="X-Axis:", background="#F5F5F5").pack(pady=5)
        self.x_axis_var = tk.StringVar()
        ttk.Combobox(side_panel, textvariable=self.x_axis_var, values=["Professors", "Classes"], state="readonly").pack(pady=5)

        ttk.Label(side_panel, text="Y-Axis:", background="#F5F5F5").pack(pady=5)
        self.y_axis_var = tk.StringVar()
        ttk.Combobox(side_panel, textvariable=self.y_axis_var, values=["% As", "% Ds/Fs"], state="readonly").pack(pady=5)

        ttk.Checkbutton(side_panel, text="Include All Faculty").pack(pady=10)
        ttk.Checkbutton(side_panel, text="Include Class Count").pack(pady=10)

        ttk.Button(side_panel, text="Show Test Graph", command=self.display_test_graph).pack(pady=15)

    def create_footer(self):
        footer = tk.Frame(self.root, bg="#F5F5F5", height=40)
        footer.pack(fill="x")

        self.status_label = tk.Label(footer, text="Status: Ready", bg="#F5F5F5", font=("Helvetica", 10))
        self.status_label.pack(side="left", padx=10)

    def handle_search(self):
        messagebox.showinfo("Search", "Search functionality will be implemented.")

    def toggle_admin_mode(self):
        messagebox.showinfo("Admin Mode", "Admin mode toggled.")

    def display_test_graph(self):
        data = {"Prof. A": 80, "Prof. B": 90, "Prof. C": 70, "Prof. D": 85}

        if self.graph_canvas:
            self.graph_canvas.get_tk_widget().destroy()

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(data.keys(), data.values(), color="#4CAF50")
        ax.set_title("Test Graph - Grade Distribution", fontsize=14)
        ax.set_ylabel("% Grades")
        ax.set_xlabel("Professors")

        self.graph_canvas = FigureCanvasTkAgg(fig, master=self.graph_area)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(fill="both", expand=True)

        self.status_label.config(text="Status: Test graph displayed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EasyAApp(root)
    root.mainloop()

