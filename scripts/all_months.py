import os
import shutil
from datetime import datetime
import exifread
from tkinter import filedialog
import socket

def on_laptop():
    hostname = socket.gethostname()
    return 'laptop' in hostname.lower()

def get_folders():
    return (
        r"G:\Other computers\My computer\ricoh\all"
        if on_laptop()
        else r"D:\ricoh\all"
    )

def get_original_date(file_path):
    with open(file_path, 'rb') as file:
        tags = exifread.process_file(file, details=False)
        date_str = tags.get('EXIF DateTimeOriginal')
        return datetime.strptime(str(date_str), '%Y:%m:%d %H:%M:%S') if date_str else None

def organise_image_files(src_folder, dest_folder):
    files_moved_count = 0
    moved_files = set()

    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.lower().endswith('.dng') or file.lower().endswith('.jpg'):
                file_path = os.path.join(root, file)
                if file_path not in moved_files:
                    original_date = get_original_date(file_path)
                    if original_date:
                        dest_path = os.path.join(dest_folder, str(original_date.year), f"{original_date.month:02d}")
                        os.makedirs(dest_path, exist_ok=True)
                        shutil.move(file_path, os.path.join(dest_path, file))
                        moved_files.add(file_path)
                        files_moved_count += 1
                        print(f"Moved: {file_path} to {os.path.join(dest_path, file)}")

    return files_moved_count

if __name__ == "__main__":
    
    # Get source folder based on the hostname
    src_folder = get_folders()

    # Ask the user to select the destination folder
    dest_folder = filedialog.askdirectory(title="Select Destination Folder")


    if src_folder:
        # Combine the source folder with the additional folders
        all_folders = (src_folder) + get_folders()

        # Organise images in all selected folders
        for folder in all_folders:
            print(f"Organising DNG and JPG files in {folder}...")
            total_files_moved = organise_image_files(folder, dest_folder)
            print(f"Organising complete. {total_files_moved} files moved.")
    else:
        print("Source folder not selected.")
