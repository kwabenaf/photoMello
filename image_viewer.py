import os
import shutil
import tkinter as tk
from tkinter import filedialog
import rawpy
from PIL import Image, ImageTk

class RawImageViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Raw Image Viewer")

        self.canvas = tk.Canvas(self.master, width=600, height=400)
        self.canvas.pack(pady=10)

        # Add a button to open a raw image
        self.open_button = tk.Button(self.master, text="Open Raw Image", command=self.open_raw_image)
        self.open_button.pack(pady=10)

        # Add a button to convert to JPEG
        self.convert_button = tk.Button(self.master, text="Convert to JPEG", command=self.convert_to_jpeg)
        self.convert_button.pack(pady=10)
        self.convert_button['state'] = 'disabled'  # Initially disable the button

        # Variable to store the path of the currently opened DNG file
        self.current_dng_path = None

    def open_raw_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Raw Image files", "*.dng")])

        if file_path:
            # Update the variable with the current DNG file path
            self.current_dng_path = file_path

            # Use rawpy to read the raw image
            with rawpy.imread(file_path) as raw:
                # Use the postprocess method to convert the raw image to RGB
                rgb_image = raw.postprocess()

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

                # Enable the "Convert to JPEG" button
                self.convert_button['state'] = 'normal'

    def convert_to_jpeg(self):
        if self.current_dng_path:
            # Get the current filename without extension
            current_filename = os.path.splitext(os.path.basename(self.current_dng_path))[0]

            # Suggest a default filename for the JPEG conversion
            suggested_filename = current_filename + '_convert.jpg'

            # Ask the user to choose a location and filename for the saved JPEG
            output_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                initialfile=suggested_filename,
                filetypes=[("JPEG files", "*.jpg")]
            )

            # Check if the user selected a location
            if output_path:
                # Use rawpy to read the raw image
                with rawpy.imread(self.current_dng_path) as raw:
                    # Set white balance (adjust these values based on your image)
                    user_wb = (2.0, 1.0, 2.0, 1.0)

                    # Perform the postprocessing with the updated parameters
                    rgb_image = raw.postprocess(user_wb=user_wb)

                    # Convert the RGB image to a PIL Image
                    pil_image = Image.fromarray(rgb_image)

                    # Save the image as JPEG with a high-quality setting
                    pil_image.save(output_path, 'JPEG', quality=100)

                    # Inform the user about the successful conversion
                    tk.messagebox.showinfo("Info", f"Conversion complete. JPEG saved at {output_path}")




if __name__ == "__main__":
    root = tk.Tk()
    raw_image_viewer = RawImageViewer(root)
    root.mainloop()
