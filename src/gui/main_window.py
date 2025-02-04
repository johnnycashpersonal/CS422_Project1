import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.data.db_manager import DatabaseManager

class DualWindowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EasyA - Grade Comparison")
        self.root.geometry("1200x800")
        self.root.configure(bg="#FFFFFF")

        # Initialize graph display settings
        self.show_class_count = True
        self.show_as = True  # True for As, False for DFs
        
        # Initialize pagination variables
        self.left_page = 0
        self.right_page = 0
        self.results_per_page = 8
        self.left_current_results = []
        self.right_current_results = []

        self.departments = [
            "ANTH",  # Anthropology
            "ASTR",  # Astronomy
            "BI",    # Biology
            "CH",    # Chemistry
            "CIS",   # Computer and Info Science
            "GEOG",  # Geography
            "GEOL",  # Geology
            "HPHY",  # Human Physiology
            "MATH",  # Mathematics
            "PHYS",  # Physics
            "PSY"    # Psychology
        ]
        
        self.course_levels = [
            "Show All", "100-level", "200-level", "300-level",
            "400-level", "500-level", "600-level"
        ]

        self.db_manager = DatabaseManager()

        # Configure global styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 12), padding=6)
        self.style.configure("TRadiobutton", font=("Helvetica", 14, "bold"), foreground="black")
        self.style.configure("TCheckbutton", font=("Helvetica", 14, "bold"), foreground="black")
        self.style.map(
            "TButton",
            foreground=[("active", "#FFFFFF")],
            background=[("active", "#4CAF50")],
        )

        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Create control panel for graph options (top)
        self.control_panel = ttk.Frame(self.main_container)
        self.control_panel.pack(fill=tk.X, padx=10, pady=5)
        self.create_graph_controls()

        # Create graph section (middle)
        self.graph_section = ttk.PanedWindow(self.main_container, orient=tk.HORIZONTAL)
        self.graph_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create left and right graph frames
        self.left_graph_frame = ttk.LabelFrame(self.graph_section, text="Left Graph")
        self.right_graph_frame = ttk.LabelFrame(self.graph_section, text="Right Graph")
        
        # Add frames to PanedWindow
        self.graph_section.add(self.left_graph_frame, weight=1)
        self.graph_section.add(self.right_graph_frame, weight=1)

        # Initialize graphs
        self.create_graph(self.left_graph_frame, "left")
        self.create_graph(self.right_graph_frame, "right")

        # Store the current search parameters for graph titles
        self.left_search_params = {}
        self.right_search_params = {}

        # Create search section (bottom)
        self.search_section = ttk.Frame(self.main_container)
        self.search_section.pack(fill=tk.X, padx=10, pady=5)
        
        # Create search parameters
        self.create_search_area(self.search_section)

        # Create footer
        self.create_footer()

    def create_graph_controls(self):
        """Create controls for graph display options"""
        # Grade type toggle
        self.grade_var = tk.StringVar(value="% As")
        ttk.Radiobutton(
            self.control_panel,
            text="Show % As",
            variable=self.grade_var,
            value="% As",
            command=self.update_all_graphs
        ).pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Radiobutton(
            self.control_panel,
            text="Show % Ds/Fs",
            variable=self.grade_var,
            value="% Ds/Fs",
            command=self.update_all_graphs
        ).pack(side=tk.LEFT, padx=10, pady=5)

        # Class count toggle
        self.count_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.control_panel,
            text="Show Class Count",
            variable=self.count_var,
            command=self.update_all_graphs
        ).pack(side=tk.LEFT, padx=20, pady=5)

    def create_graph(self, parent, side):
        """Create a matplotlib graph in the given frame"""
        # Create container for graph and navigation
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Create navigation buttons at the top
        nav_frame = ttk.Frame(container)
        nav_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            nav_frame, 
            text="← Previous", 
            command=lambda: self.change_page(side, -1)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            nav_frame, 
            text="Next →", 
            command=lambda: self.change_page(side, 1)
        ).pack(side=tk.RIGHT, padx=5)
        
        # Add page indicator label
        page_label = ttk.Label(nav_frame, text="Page 1")
        page_label.pack(side=tk.TOP, pady=5)
        if side == "left":
            self.left_page_label = page_label
        else:
            self.right_page_label = page_label
        
        # Create the graph
        fig = Figure(figsize=(6, 4), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        if side == "left":
            self.left_fig = fig
            self.left_canvas = canvas
        else:
            self.right_fig = fig
            self.right_canvas = canvas

    def create_search_area(self, parent):
        """Create search parameters area"""
        left_search = ttk.LabelFrame(parent, text="Left Side Search")
        right_search = ttk.LabelFrame(parent, text="Right Side Search")
        
        left_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        right_search.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5, pady=5)
        
        self.create_search_fields(left_search, "left")
        self.create_search_fields(right_search, "right")

    def create_search_fields(self, parent, side):
        """Create search fields for one side"""
        if side == "left":
            self.left_entries = {}
            entries = self.left_entries
        else:
            self.right_entries = {}
            entries = self.right_entries

        ttk.Label(parent, text="Department:").grid(row=0, column=0, padx=5, pady=5)
        entries['department'] = ttk.Combobox(parent, width=15, values=self.departments, state="readonly")
        entries['department'].grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Course Level:").grid(row=0, column=2, padx=5, pady=5)
        entries['level'] = ttk.Combobox(parent, width=15, values=self.course_levels, state="readonly")
        entries['level'].grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(parent, text="Class Number:").grid(row=1, column=0, padx=5, pady=5)
        entries['class'] = ttk.Entry(parent, width=10)
        entries['class'].grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Year:").grid(row=1, column=2, padx=5, pady=5)
        entries['year'] = ttk.Entry(parent, width=8)
        entries['year'].grid(row=1, column=3, padx=5, pady=5)

        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Search", 
                  command=lambda s=side: self.handle_search(s)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Search by Level", 
                  command=lambda s=side: self.handle_level_search(s)).pack(side=tk.LEFT, padx=5)

    def create_footer(self):
        """Create footer with status and admin button"""
        footer = ttk.Frame(self.root)
        footer.pack(fill="x", side="bottom", padx=5, pady=5)

        self.status_label = ttk.Label(footer, text="Status: Ready")
        self.status_label.pack(side="left", padx=5)


    def get_graph_title(self, side):
        """Generate graph title based on search parameters"""
        entries = self.left_entries if side == "left" else self.right_entries
        params = {}
        
        dept = entries['department'].get()
        level = entries['level'].get()
        class_num = entries['class'].get()
        year = entries['year'].get()
        
        title_parts = []
        if dept:
            title_parts.append(f"Dept: {dept}")
        if class_num:
            title_parts.append(f"Course: {class_num}")
        if level and level != "Show All":
            title_parts.append(f"Level: {level}")
        if year:
            title_parts.append(f"Year: {year}")
            
        return " | ".join(title_parts) if title_parts else "No Search Parameters"

    def update_all_graphs(self):
        """Update both graphs with current display settings"""
        self.show_as = self.grade_var.get() == "% As"
        self.show_class_count = self.count_var.get()
        
        if hasattr(self, 'left_current_results'):
            self.update_side_graph('left', self.left_current_results)
        if hasattr(self, 'right_current_results'):
            self.update_side_graph('right', self.right_current_results)

    def change_page(self, side, direction):
        """Change the current page for the specified side
        Args:
            side (str): 'left' or 'right'
            direction (int): 1 for next page, -1 for previous page
        """
        if side == "left":
            results = self.left_current_results
            current_page = self.left_page
        else:
            results = self.right_current_results
            current_page = self.right_page
        
        total_pages = (len(results) - 1) // self.results_per_page + 1
        new_page = current_page + direction
        
        if 0 <= new_page < total_pages:
            if side == "left":
                self.left_page = new_page
                self.left_page_label.config(text=f"Page {new_page + 1} of {total_pages}")
            else:
                self.right_page = new_page
                self.right_page_label.config(text=f"Page {new_page + 1} of {total_pages}")
            
            self.update_side_graph(side, results)

    def handle_search(self, side):
        """Handle search by course number"""
        entries = self.left_entries if side == "left" else self.right_entries
        
        department = entries['department'].get().strip()
        class_num = entries['class'].get().strip()
        year = entries['year'].get().strip()
        
        try:
            if not department:
                messagebox.showerror("Error", "Please select a department")
                return
                
            course_id = department + class_num if class_num else None
            
            # Modify pipeline to group by instructor if searching for specific course
            if course_id:
                match_conditions = {"course_id": course_id}
                if year:
                    try:
                        year_num = int(year)
                        match_conditions["year"] = year_num
                    except ValueError:
                        messagebox.showerror("Error", "Year must be a valid number")
                        return
                        
                pipeline = [
                    {"$match": match_conditions},
                    {"$group": {
                        "_id": "$instructor_name",
                        "avg_percent_a": {"$avg": "$percent_a"},
                        "avg_percent_df": {"$avg": "$percent_df"},
                        "class_count": {"$sum": 1}
                    }},
                    {"$sort": {"avg_percent_a": -1}}
                ]
                
                results = list(self.db_manager.grade_distributions.aggregate(pipeline))
            else:
                # For department-wide search, use existing department stats
                results = self.db_manager.get_department_stats(department)
                
            # Reset pagination and store current results
            if side == "left":
                self.left_page = 0
                self.left_current_results = results
            else:
                self.right_page = 0
                self.right_current_results = results
                
            self.update_side_graph(side, results)
            total_pages = (len(results) - 1) // self.results_per_page + 1
            self.status_label.config(text=f"Status: Found {len(results)} results ({total_pages} pages)")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Status: Error fetching data")

    def handle_level_search(self, side):
        """Handle search by course level"""
        entries = self.left_entries if side == "left" else self.right_entries
        
        department = entries['department'].get().strip()
        level_text = entries['level'].get().strip()
        year = entries['year'].get().strip()
        
        if not department or not level_text:
            messagebox.showerror("Error", "Please select both department and course level")
            return
            
        try:
            regex_pattern = f"^{department}"
            if level_text != "Show All":
                level_num = level_text[0]
                regex_pattern = f"^{department}{level_num}"
                
            # Add year filter to pipeline if year is provided
            match_conditions = {"course_id": {"$regex": regex_pattern}}
            if year:
                try:
                    year_num = int(year)
                    match_conditions["year"] = year_num
                except ValueError:
                    messagebox.showerror("Error", "Year must be a valid number")
                    return
                    
            pipeline = [
                {"$match": match_conditions},
                {"$group": {
                    "_id": "$course_id",
                    "avg_percent_a": {"$avg": "$percent_a"},
                    "avg_percent_df": {"$avg": "$percent_df"},
                    "class_count": {"$sum": 1},
                    "instructors": {"$addToSet": "$instructor_name"}
                }},
                {"$sort": {"avg_percent_a": -1}}
            ]
            
            results = list(self.db_manager.grade_distributions.aggregate(pipeline))
            
            # Reset pagination when new search is performed
            if side == "left":
                self.left_page = 0
                self.left_current_results = results
            else:
                self.right_page = 0
                self.right_current_results = results
                
            self.update_side_graph(side, results)
            total_pages = (len(results) - 1) // self.results_per_page + 1
            self.status_label.config(text=f"Status: Found {len(results)} results ({total_pages} pages)")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Status: Error fetching data")

    def update_side_graph(self, side, results):
        """Update graph for one side with the search results"""
        fig = self.left_fig if side == "left" else self.right_fig
        canvas = self.left_canvas if side == "left" else self.right_canvas
        current_page = self.left_page if side == "left" else self.right_page
        
        # Calculate slice indices for current page
        start_idx = current_page * self.results_per_page
        end_idx = start_idx + self.results_per_page
        page_results = results[start_idx:end_idx]
        
        fig.clear()
        ax = fig.add_subplot(111)
        
        # Extract data for plotting
        courses = [r["_id"] for r in page_results]
        percentages = [r['avg_percent_a' if self.show_as else 'avg_percent_df'] for r in page_results]
        counts = [r['class_count'] for r in page_results]
        
        # Create bars
        bars = ax.bar(range(len(courses)), percentages, 
                    color='blue' if side == "left" else 'red', alpha=0.7)
        
        # Add class count labels if enabled
        if self.show_class_count:
            for bar, count in zip(bars, counts):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'n={count}',
                    ha='center', va='bottom')
        
        # Customize the graph
        ax.set_ylabel("% As" if self.show_as else "% Ds/Fs")
        ax.set_title(self.get_graph_title(side))
        ax.set_xticks(range(len(courses)))
        ax.set_xticklabels(courses, rotation=45, ha='right')
        
        # Add grid for better readability
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Set y-axis limits
        ax.set_ylim(0, 100)
        
        # Update page indicator
        total_pages = (len(results) - 1) // self.results_per_page + 1
        page_label = self.left_page_label if side == "left" else self.right_page_label
        page_label.config(text=f"Page {current_page + 1} of {total_pages}")
        
        fig.tight_layout()
        canvas.draw()

    def toggle_admin_mode(self):
        """Toggle admin mode"""
        messagebox.showinfo("Admin Mode", "Admin mode toggled.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DualWindowApp(root)
    root.mainloop()


