import os
import shutil
import numpy as np
import tkinter as tk
from tkinter import messagebox
import rawpy
from PIL import Image, ImageTk

class RawImageViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Organise photos")

        self.canvas = tk.Canvas(self.master, width=600, height=400)
        self.canvas.pack(pady=10)

        # Add a label for file number indicator (hidden initially)
        self.file_indicator_label = tk.Label(self.master, text="")
        self.file_indicator_label.pack(pady=10)
        self.file_indicator_label.pack_forget()

        # Add a button to open a raw image
        self.open_button = tk.Button(self.master, text="open sort", command=self.open_raw_image)
        self.open_button.pack(pady=10)

        # Variable to store the path of the currently opened DNG file
        self.current_dng_path = None

        # List to store all raw image files in the folder
        self.raw_image_files = []
        # Index to keep track of the current image in the list
        self.current_image_index = 0

    def open_raw_image(self):
        folder_path = r"D:\ricoh\all\sort"

        # Get a list of all raw image files in the folder
        self.raw_image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.dng', '.jpg'))]

        if self.raw_image_files:
            # Set the file path to the first image in the list
            file_path = os.path.join(folder_path, self.raw_image_files[0])

            # Update the variable with the current DNG file path
            self.current_dng_path = file_path

            # Find the index of the current image in the list
            self.current_image_index = 0

            # Display the current image
            self.display_image()

        
    def display_image(self):
        # Check if the current image file exists
        current_file_path = os.path.join(os.path.dirname(self.current_dng_path), self.raw_image_files[self.current_image_index])

        if not os.path.isfile(current_file_path):
            # If the file doesn't exist, move to the next available image
            self.navigate_images("right")
            return

        # Check file extension
        _, file_extension = os.path.splitext(current_file_path)

        if file_extension.lower() == '.dng':
            # Use rawpy to read the raw image
            with rawpy.imread(current_file_path) as raw:
                # Use the postprocess method to convert the raw image to RGB
                rgb_image = raw.postprocess()
        else:
            # For other file formats (e.g., .jpg), directly open the image with PIL
            pil_image = Image.open(current_file_path)

            # Convert PIL image to a NumPy array
            rgb_image = np.array(pil_image)

        # Convert the RGB image to a PIL Image
        pil_image = Image.fromarray(rgb_image)

        # Resize the image for display with a 3:2 aspect ratio
        target_width = 600
        target_height = int((2 / 3) * target_width)
        pil_image = pil_image.resize((target_width, target_height), Image.BICUBIC)

        # Display the image using Tkinter
        photo = ImageTk.PhotoImage(pil_image)
        self.canvas.config(width=pil_image.width, height=pil_image.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

        # Update the file indicator
        self.update_file_indicator()


    def navigate_images(self, direction):
        # Update the current image index based on the direction
        if direction == "left":
            self.current_image_index = (self.current_image_index - 1) % len(self.raw_image_files)
        elif direction == "right":
            self.current_image_index = (self.current_image_index + 1) % len(self.raw_image_files)

        # Display the new image
        self.display_image()

        # If the move was triggered by a refresh, do not perform automatic movement
        if not hasattr(self, 'refresh_triggered') or not self.refresh_triggered:
            # Perform the automatic movement (if any)
            # Add your automatic movement functionality here

        # Reset the refresh flag
            self.refresh_triggered = False


    def move_and_display_message(self, destination_folder, message):
        source_path = os.path.join(os.path.dirname(self.current_dng_path), self.raw_image_files[self.current_image_index])

        try:
            shutil.move(source_path, destination_folder)
        except Exception as e:
            messagebox.showerror("Error", f"Error moving file: {str(e)}")
            return

        # Show message in a pop-up
        messagebox.showinfo("Info", message)
        print(f"saved into {destination_folder}")

        # Update the file indicator
        self.update_file_indicator()

        # Refresh the list of raw image files
        folder_path = os.path.dirname(self.current_dng_path)
        self.raw_image_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.dng')]

        # Set the refresh flag
        self.refresh_triggered = True

        # Display the next image
        self.navigate_images("right")

    def save_message(self):
        self.move_and_display_message(r"D:\ricoh\all", "Saved")

    def achieve_message(self):
        self.move_and_display_message(r"D:\ricoh\archive", "Achieved")

    def update_file_indicator(self):
        # Update the file indicator label
        current_file_no = self.current_image_index + 1
        total_files = len(self.raw_image_files)
        self.file_indicator_label.config(text=f"Image {current_file_no}/{total_files}")

        # Show the file indicator label after an image is selected
        self.file_indicator_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    raw_image_viewer = RawImageViewer(root)

    # Bind left and right arrow key events to navigate_images method
    root.bind("<Left>", lambda event: raw_image_viewer.navigate_images("left"))
    root.bind("<Right>", lambda event: raw_image_viewer.navigate_images("right"))

    # Bind up and down arrow key events to save_message and achieve_message methods
    root.bind("<Up>", lambda event: raw_image_viewer.save_message())
    root.bind("<Down>", lambda event: raw_image_viewer.achieve_message())

    root.mainloop()
