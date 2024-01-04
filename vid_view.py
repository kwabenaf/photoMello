import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import imageio
import rawpy

class FileViewer:
    def __init__(self, root):
        self.root = root
        self.files = []
        self.current_index = 0
        self.is_playing = False
        self.canvas_image = None

        self.canvas = tk.Canvas(root)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        
        self.btn_previous = tk.Button(root, text="Previous", command=self.show_previous)
        self.btn_previous.pack(side=tk.LEFT)

        self.btn_play_pause = tk.Button(root, text="Play", command=self.toggle_play)
        self.btn_play_pause.pack(side=tk.LEFT)

        self.btn_next = tk.Button(root, text="Next", command=self.show_next)
        self.btn_next.pack(side=tk.LEFT)

        self.btn_open_folder = tk.Button(root, text="Open Folder", command=self.open_folder)
        self.btn_open_folder.pack(side=tk.LEFT)

        self.load_file()

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]
            self.current_index = 0
            self.load_file()

    def load_file(self):
        if not self.files:
            print("No files in the folder.")
            return

        # Clear previous canvas items
        self.canvas.delete("all")

        file_path = self.files[self.current_index]

        try:
            if file_path.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                # Load regular image
                image = Image.open(file_path)
                photo = ImageTk.PhotoImage(image)
                self.canvas.config(width=photo.width(), height=photo.height())
                self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                self.root.title(f"Image Viewer - {os.path.basename(file_path)}")

            elif file_path.lower().endswith((".avi", ".mp4", ".mkv")):
                # Load video
                video = imageio.get_reader(file_path)
                self.video_iter = iter(video)
                self.video_frames = [ImageTk.PhotoImage(Image.fromarray(frame)) for frame in video]

                self.canvas.config(width=self.video_frames[0].width(), height=self.video_frames[0].height())
                self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.video_frames[0])
                self.root.title(f"Video Viewer - {os.path.basename(file_path)}")

            elif file_path.lower().endswith(".dng"):
                # Load DNG using rawpy
                with rawpy.imread(file_path) as raw:
                    rgb = raw.postprocess()
                    image = Image.fromarray(rgb)
                    photo = ImageTk.PhotoImage(image)
                    self.canvas.config(width=photo.width(), height=photo.height())
                    self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                    self.root.title(f"Image Viewer - {os.path.basename(file_path)}")

            else:
                print("Unsupported file format")

        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            # Add an additional print statement to check the exception type
            import traceback
            traceback.print_exc()

        # Ensure that buttons are always visible
        self.btn_previous.pack(side=tk.LEFT)
        self.btn_play_pause.pack(side=tk.LEFT)
        self.btn_next.pack(side=tk.LEFT)
        self.btn_open_folder.pack(side=tk.LEFT)

    def show_previous(self):
        self.current_index = (self.current_index - 1) % len(self.files)
        self.load_file()

    def show_next(self):
        self.current_index = (self.current_index + 1) % len(self.files)
        self.load_file()

    def toggle_play(self):
        if self.is_playing:
            self.btn_play_pause.config(text="Play")
            self.is_playing = False
            self.root.after_cancel(self.play_next_frame)
        else:
            self.btn_play_pause.config(text="Pause")
            self.is_playing = True
            self.play_next_frame()

    def play_next_frame(self):
        if self.is_playing:
            try:
                frame = next(self.video_iter)
                photo = ImageTk.PhotoImage(Image.fromarray(frame))
                self.canvas.itemconfig(self.canvas_image, image=photo)
                self.canvas.image = photo
                self.root.after(50, self.play_next_frame)
            except StopIteration:
                self.is_playing = False
                self.btn_play_pause.config(text="Play")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Viewer")

    # Set a reasonable window size
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    viewer = FileViewer(root)
    root.mainloop()
