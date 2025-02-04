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
        self.root.geometry("1800x900")
        self.root.configure(bg="#FFFFFF")

        # Add department options
        self.departments = [
            "BI",    # Biology
            "CH",    # Chemistry
            "CIS",   # Computer and Info Science
            "HPHY",  # Human Physiology
            "MATH",  # Mathematics
            "PHYS",  # Physics
            "PSY"    # Psychology
        ]
        
        # Add course levels with Show All option
        self.course_levels = [
            "Show All",
            "100-level",
            "200-level",
            "300-level",
            "400-level",
            "500-level",
            "600-level"
        ]

        self.db_manager = DatabaseManager()

        # Configure global styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 12), padding=6)
        self.style.map(
            "TButton",
            foreground=[("active", "#FFFFFF")],
            background=[("active", "#4CAF50")],
        )

        # Create main container as PanedWindow
        self.main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Create left and right frames
        self.left_frame = ttk.Frame(self.main_container)
        self.right_frame = ttk.Frame(self.main_container)
        
        # Add frames to PanedWindow
        self.main_container.add(self.left_frame, weight=1)
        self.main_container.add(self.right_frame, weight=1)

        # Create headers for both sides
        self.create_header(self.left_frame, "left")
        self.create_header(self.right_frame, "right")

        # Create main areas for both sides
        self.create_main_area(self.left_frame, "left")
        self.create_main_area(self.right_frame, "right")

        # Create shared footer
        self.create_footer()

        # Configure weight for proper resizing
        self.left_frame.columnconfigure(0, weight=1)
        self.right_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def create_header(self, parent, side):
        header = ttk.Frame(parent)
        header.pack(fill="x", padx=5, pady=5)

        # Store entry widgets in dictionaries for easy access
        if side == "left":
            self.left_entries = {}
        else:
            self.right_entries = {}
        
        entries = self.left_entries if side == "left" else self.right_entries

        # Create a sub-frame for better organization
        fields_frame = ttk.Frame(header)
        fields_frame.pack(fill="x")

        # Department field (dropdown)
        dept_frame = ttk.Frame(fields_frame)
        dept_frame.pack(side="left", padx=5)
        ttk.Label(dept_frame, text="Department:").pack(side="left")
        entries['department'] = ttk.Combobox(dept_frame, width=15, values=self.departments, state="readonly")
        entries['department'].pack(side="left", padx=2)

        # Course Level field (dropdown)
        level_frame = ttk.Frame(fields_frame)
        level_frame.pack(side="left", padx=5)
        ttk.Label(level_frame, text="Course Level:").pack(side="left")
        entries['level'] = ttk.Combobox(level_frame, width=15, values=self.course_levels, state="readonly")
        entries['level'].pack(side="left", padx=2)

        # Class Number field
        class_frame = ttk.Frame(fields_frame)
        class_frame.pack(side="left", padx=5)
        ttk.Label(class_frame, text="Class Number:").pack(side="left")
        entries['class'] = ttk.Entry(class_frame, width=10)
        entries['class'].pack(side="left", padx=2)

        # Year field
        year_frame = ttk.Frame(fields_frame)
        year_frame.pack(side="left", padx=5)
        ttk.Label(year_frame, text="Year:").pack(side="left")
        entries['year'] = ttk.Entry(year_frame, width=8)
        entries['year'].pack(side="left", padx=2)

        # Buttons frame
        buttons_frame = ttk.Frame(fields_frame)
        buttons_frame.pack(side="left", padx=5)
        
        # Search buttons
        ttk.Button(buttons_frame, text="Search", 
                  command=lambda s=side: self.handle_search(s)).pack(side="left", padx=2)
        ttk.Button(buttons_frame, text="Search by Level", 
                  command=lambda s=side: self.handle_level_search(s)).pack(side="left", padx=2)

    def create_main_area(self, parent, side):
        # Create frame for the main area that will expand
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure the main frame to expand properly
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Create and configure the treeview with scrollbar
        tree = ttk.Treeview(main_frame, columns=("Professor", "Course", "%As", "%DFs", "Count"), 
                           show="headings", selectmode="extended")
        
        # Create scrollbars
        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Grid layout for tree and scrollbars
        tree.grid(column=0, row=0, sticky="nsew")
        vsb.grid(column=1, row=0, sticky="ns")
        hsb.grid(column=0, row=1, sticky="ew")

        # Configure column headings
        tree.heading("Professor", text="Professor")
        tree.heading("Course", text="Course")
        tree.heading("%As", text="% As")
        tree.heading("%DFs", text="% D/Fs")
        tree.heading("Count", text="Class Count")

        # Configure column widths
        for col in ("Professor", "Course", "%As", "%DFs", "Count"):
            tree.column(col, width=100, minwidth=50)

        # Store the tree reference
        if side == "left":
            self.left_tree = tree
        else:
            self.right_tree = tree

    def create_footer(self):
        footer = ttk.Frame(self.root)
        footer.pack(fill="x", side="bottom", padx=5, pady=5)

        self.status_label = ttk.Label(footer, text="Status: Ready")
        self.status_label.pack(side="left", padx=5)

        ttk.Button(footer, text="Admin Mode", 
                  command=self.toggle_admin_mode).pack(side="right", padx=5)

    def handle_search(self, side):
        entries = self.left_entries if side == "left" else self.right_entries
        tree = self.left_tree if side == "left" else self.right_tree
        
        department = entries['department'].get().strip()
        class_num = entries['class'].get().strip()
        
        # Clear existing entries
        for item in tree.get_children():
            tree.delete(item)
            
        try:
            if not department:
                messagebox.showerror("Error", "Please select a department")
                return
                
            course_id = department + class_num if class_num else None
            
            # Get data based on search criteria
            results = []
            if course_id:
                results = self.db_manager.get_course_stats(course_id)
            else:
                results = self.db_manager.get_department_stats(department)
                
            # Insert data into table
            for result in results:
                tree.insert("", "end", values=(
                    result["_id"],
                    course_id if course_id else department,
                    f"{result['avg_percent_a']:.1f}",
                    f"{result['avg_percent_df']:.1f}",
                    result["class_count"]
                ))
                
            self.status_label.config(text=f"Status: Found {len(results)} results")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Status: Error fetching data")

    def handle_level_search(self, side):
        entries = self.left_entries if side == "left" else self.right_entries
        tree = self.left_tree if side == "left" else self.right_tree
        
        department = entries['department'].get().strip()
        level_text = entries['level'].get().strip()
        
        if not department:
            messagebox.showerror("Error", "Please select a department")
            return
            
        if not level_text:
            messagebox.showerror("Error", "Please select a course level")
            return
            
        # Clear existing entries
        for item in tree.get_children():
            tree.delete(item)
            
        try:
            # Modify pipeline based on whether "Show All" is selected
            if level_text == "Show All":
                # Show all courses for the department
                regex_pattern = f"^{department}"
            else:
                # Extract the level number and filter by it
                level_num = level_text[0]
                regex_pattern = f"^{department}{level_num}"
                
            pipeline = [
                {"$match": {
                    "course_id": {
                        "$regex": regex_pattern
                    }
                }},
                {"$group": {
                    "_id": {
                        "instructor": "$instructor_name",
                        "course": "$course_id"
                    },
                    "avg_percent_a": {"$avg": "$percent_a"},
                    "avg_percent_df": {"$avg": "$percent_df"},
                    "class_count": {"$sum": 1}
                }},
                {"$sort": {"_id.course": 1, "_id.instructor": 1}}
            ]
            
            results = list(self.db_manager.grade_distributions.aggregate(pipeline))
            
            for result in results:
                tree.insert("", "end", values=(
                    result["_id"]["instructor"],
                    result["_id"]["course"],
                    f"{result['avg_percent_a']:.1f}",
                    f"{result['avg_percent_df']:.1f}",
                    result["class_count"]
                ))
            
            self.status_label.config(text=f"Status: Found {len(results)} results")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Status: Error fetching data")

    def toggle_admin_mode(self):
        messagebox.showinfo("Admin Mode", "Admin mode toggled.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DualWindowApp(root)
    root.mainloop()