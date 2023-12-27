import os
import keyboard
import shutil
import socket
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from image_viewer import RawImageViewer  # Import RawImageViewer from image_viewer.py


# CHECK IF RUNNING ON LAPTOP
def on_laptop():
    # Get the hostname of the machine
    hostname = socket.gethostname()

    # Check if the hostname indicates that the script is running on the laptop
    return 'laptop' in hostname.lower()
    





class PhotoMello:
    """
    A class representing the photoMello application.

    Methods:
    - __init__: Initializes the application.
    - on_close: Handles the window close event.
    - open_image: Opens and displays an image in a new window.
    - import_photos: Imports photos from a selected folder to a destination folder.
    - organise_photos: Organises photos in a new window.
    - convert_jpeg: Converts images to JPEG format.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("photoMello")

        self.cancel_operation = False

        # Create buttons for different functionalities
        self.import_button = tk.Button(root, text="Import Photos", command=self.import_photos)
        self.organise_button = tk.Button(root, text="Organise Photos", command=self.organise_photos)
        self.convert_button = tk.Button(root, text="Convert > JPEG", command=self.convert_jpeg)

        # Pack the buttons
        self.import_button.pack(pady=20)
        self.organise_button.pack(pady=20)
        self.convert_button.pack(pady=20)


 # Create a Canvas for the image
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack(pady=10)

# POSITIONING APP
# Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the position for the window
        x_position = (screen_width - 400) // 2  # Adjust 400 based on your window width
        y_position = (screen_height - 200) // 2  # Adjust 200 based on your window height

        # Set the window position
        self.root.geometry(f"400x200+{x_position}+{y_position}")
 

 # CLOSING APP   
    # Bind the window close event to the on_close method
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Add any cleanup code here before closing the window
        self.root.destroy()


    def open_image(self):
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.dng")])

            if file_path:
                # Open and display the image using Pillow
                image = Image.open(file_path)
                image = image.resize((600, 400), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)

                # Update the Canvas with the new image
                self.canvas.config(width=image.width, height=image.height)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                self.canvas.image = photo


# IMPORT IMAGES
    def import_photos(self):

    # Check if the user selected a folder
        if source_folder := filedialog.askdirectory(title="Select Source Folder"):
            # Specify the paths of the additional folders to check for duplicates
            self.additional_folders = {
                'pc': [
                    r"D:\ricoh\all",
                    r"D:\ricoh\archive",
                    r"D:\ricoh\print-ready"
                    
                ],
                'laptop': [
                    r"G:\Other computers\My computer\ricoh\all",
                    r"G:\Other computers\My computer\ricoh\archive",
                    r"G:\Other computers\My computer\ricoh\print-ready"
                ]
            }

            # Check if the additional folders exist for the current environment
            for folder in self.additional_folders.get('laptop' if on_laptop() else 'pc', []):
                print(f"Checking folder: {folder}")
                if not any(os.path.exists(os.path.join(folder, subfolder)) for subfolder in os.listdir(folder)):
                    tk.messagebox.showerror("Error", f"Folder '{folder}' or its subfolders do not exist.")
                    return

            # Specify the destination folder based on the environment
            destination_folders = {
                'pc': r"D:\ricoh\all",
                'laptop': r"G:\Other computers\My computer\ricoh\all"
            }

            destination_folder = destination_folders.get('laptop' if on_laptop() else 'pc')

            # Ensure the destination folder exists
            os.makedirs(destination_folder, exist_ok=True)
            

            # Function to listen for the "ESC" key press
            def check_for_cancel(e):
                root.after(0, lambda: keyboard.unhook(check_for_cancel))
                tk.messagebox.showinfo("Info", "Operation canceled.")

            # Function to copy a file
            def copy_file(source_path, destination_path):
                shutil.copy(source_path, destination_path)

            # Function to import photos
            def import_photos_internal():

                # Get a set of files in all additional folders
                additional_files = set()
                for folder in self.additional_folders.get('laptop' if on_laptop() else 'pc', []):
                    if os.path.exists(folder):
                        for root, dirs, files in os.walk(folder):
                            additional_files.update(files)

                # Get a set of files in the destination folder
                destination_files = set(os.listdir(destination_folder))

                # Iterate through files in the source folder and its subdirectories
                for root, dirs, files in os.walk(source_folder):
                    for filename in files:
                        if filename.lower().endswith('.dng') and not self.cancel_operation:
                            source_path = os.path.join(root, filename)
                            destination_path = os.path.join(destination_folder, filename)

                            # Check if the file already exists in the other folders
                            if filename in destination_files or filename in additional_files:
                                print(f"Skipping duplicate file: {filename}")
                            else:
                                # Copy the .DNG file to the destination folder
                                copy_file(source_path, destination_path)
                                print(f"File copied: {filename}")

                if not self.cancel_operation:
                    tk.messagebox.showinfo("Info", f"Operation complete. {len(os.listdir(destination_folder))} .DNG files copied to the destination folder.")

            # Listen for the "ESC" key press to cancel the operation
            keyboard.on_press_key('esc', check_for_cancel)

            # Import photos from the source folder to the destination folder
            import_photos_internal()


# ORGANISE PHOTOS
    def organise_photos(self):
        image_view = tk.Toplevel(self.root)
        image_view.title("Image View")
        print("Organising photos...")

        # Add a button to go back
        btn_back = tk.Button(image_view, text="Back", command=image_view.destroy)
        btn_back.pack(pady=10)


# CONVERT IMAGE TO JPEG
    def convert_jpeg(self):
        # Create a new window for Raw Image Viewer
        raw_viewer_window = tk.Toplevel(self.root)
        raw_viewer_window.title("Raw Image Viewer")

        # Create an instance of RawImageViewer in the new window
        raw_image_viewer = RawImageViewer(raw_viewer_window)

        
if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoMello(root)
    root.mainloop()
