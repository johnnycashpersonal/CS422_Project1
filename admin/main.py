import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
from src.data.db_manager import DatabaseManager
from admin.import_data import DataImporter
import admin.scrape_faculty
from admin.resolve_discrepancies import NameStandardizer

# Initialize database manager and data importer
db = DatabaseManager()
importer = DataImporter(db)

class AdminWindow:
    """
    GUI application for selecting data files and initiating faculty scraping.
    """
    def __init__(self, root):
        self.root = root

        self.root.title("File Selector App")
        self.root.geometry("300x200")

        self.root.configure(bg="#FFFFFF")
        
        self.style = ttk.Style()
        self.configure_styles()
        
        # select a data file
        self.select_button = ttk.Button(root, text="Select Data", command=self.select_file)
        self.select_button.pack(pady=10)
        
        # faculty scraping
        self.print_button = ttk.Button(root, text="Scrape for faculty", command=self.scrape_faculty)
        self.print_button.pack(pady=10)
        
        # resolve discrepancies
        self.resolve_button = ttk.Button(root, text="Resolve Discrepancies", command=self.run_resolve_discrepancies)
        self.resolve_button.pack(pady=10)
    
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
        self.print_button.config(text="Scrape for faculty")
        print("Scrape for faculty complete")
    
    def run_resolve_discrepancies(self):
        """Runs the resolve_discrepancies.py script."""
        self.resolve_button.config(text="Working...")
        print("Working (this will take some time)...")
        standardizer = NameStandardizer("faculty_list.txt")
        standardizer.update_db_instructors()
        print("DONE.")
        self.resolve_button.config(text="Resolve Discrepancies")
    
        

def main():
    root = tk.Tk()
    app = AdminWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()