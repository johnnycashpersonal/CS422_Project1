import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import admin.resolve_discrepancies
from src.data.db_manager import DatabaseManager
from admin.import_data import DataImporter
import admin.scrape_faculty
import admin.resolve_discrepancies

# Initialize database manager and data importer
db = DatabaseManager()
importer = DataImporter(db)

class AdminWindow:
    """
    GUI application for selecting data files and initiating faculty scraping.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Admininstrator")
        self.root.geometry("300x150")
        self.root.configure(bg="#FFFFFF")
        
        self.style = ttk.Style()
        self.configure_styles()
        
        # select a data file
        self.select_button = ttk.Button(root, text="Select Data", command=self.select_file)
        self.select_button.pack(pady=10)
        
        # faculty scraping
        self.print_button = ttk.Button(root, text="Scrape for faculty", command=self.scrape_faculty)
        self.print_button.pack(pady=10)
    
    def configure_styles(self):
        """Configures the styles for UI elements."""
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 12), padding=6)
        self.style.configure("TRadiobutton", font=("Helvetica", 14, "bold"), foreground="black")
        self.style.configure("TCheckbutton", font=("Helvetica", 14, "bold"), foreground="black")
        self.style.map("TButton", foreground=[("active", "#FFFFFF")], background=[("active", "#4CAF50")])
    
    def select_file(self):
        """Opens a file dialog to select a data file and imports the data."""
        file_path = filedialog.askopenfilename()
        if file_path:
            # Clear existing data in the database before importing new data
            db.courses.delete_many({})
            db.instructors.delete_many({})
            db.grade_distributions.delete_many({})
            
            print(f"Selected file: {file_path}")
            status = importer.import_grade_data(file_path)
            
            if status:
                messagebox.showinfo("Data Import", "Data imported successfully.")
            else:
                messagebox.showinfo("Data Import", "Data import failed.")
    
    def scrape_faculty(self):
        """Triggers faculty data scraping."""
        self.print_button.config(text="Working...")
        print("Faculty scraping initiated.")
        print("Working...")
        admin.scrape_faculty.main()
        admin.resolve_discrepancies.main()
        
        self.print_button.config(text="Scrape for faculty")

def main():
    root = tk.Tk()
    app = AdminWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()