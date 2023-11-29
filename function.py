import os
import shutil
import tkinter as tk
from tkinter import filedialog
from collections import Counter

class PhotoMelloGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("photoMello")

        # Create buttons
        self.import_button = tk.Button(root, text="Import Photos", command=self.import_photos)
        self.organize_button = tk.Button(root, text="Organize Photos", command=self.organize_photos)
        self.duplicate_button = tk.Button(root, text="Handle Duplicates", command=self.handle_duplicates)

        # Grid layout
        self.import_button.grid(row=0, column=0, padx=10, pady=10)
        self.organize_button.grid(row=0, column=1, padx=10, pady=10)
        self.duplicate_button.grid(row=0, column=2, padx=10, pady=10)

        # Initialize PhotoMello instance
        self.photo_mello = PhotoMello()

    def import_photos(self):
        file_paths = filedialog.askopenfilenames(title="Select Photos", filetypes=[("Image files", "*.jpg;*.png;*.dng")])
        self.photo_mello.import_photos(file_paths)

    def organize_photos(self):
        self.photo_mello.organize_photos()

    def handle_duplicates(self):
        self.photo_mello.handle_duplicates()

class PhotoMello:
    def __init__(self):
        self.unsorted_pile = []
        self.archive_pile = []
        self.save_pile = []

    def import_photos(self, file_paths):
        for file_path in file_paths:
            file_format = file_path.split('.')[-1].lower()

            if file_format == 'dng':
                self.unsorted_pile.append(file_path)
                print(f"Imported {file_path} into the unsorted pile.")
            else:
                print(f"Unsupported file format: {file_format}")

    def organize_photos(self):
        for photo_path in self.unsorted_pile:
            filename = os.path.basename(photo_path)
            event_name = "Event1"

            if "event" in filename.lower():
                self.archive_pile.append(photo_path)
                print(f"Organized {photo_path} into the archive pile.")
            else:
                self.save_pile.append(photo_path)
                print(f"Organized {photo_path} into the save pile.")

    def handle_duplicates(self):
        # Use Counter for efficient duplicate checking
        photo_counter = Counter(self.unsorted_pile)
        duplicate_files = [item for item, count in photo_counter.items() if count > 1]

        if duplicate_files:
            print("Potential duplicate photos found:")
            for duplicate in duplicate_files:
                print(f"- {duplicate}")

            user_choice = input("Do you want to delete duplicates? (yes/no): ").lower()
            if user_choice == 'yes':
                # Keep only one instance of each duplicate
                self.unsorted_pile = list(photo_counter.keys())
                print("Duplicates deleted.")
            else:
                print("Duplicates not deleted.")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoMelloGUI(root)
    root.mainloop()
