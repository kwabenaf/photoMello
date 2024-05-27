import os
import shutil
from datetime import datetime
import exifread
import socket
import keyboard

def on_laptop():
    hostname = socket.gethostname()
    return 'laptop' in hostname.lower()

def get_folders():
    return (
        r"G:\Other computers\My computer\ricoh"
        if on_laptop()
        else r"D:\ricoh"
    )

def get_original_date(file_path):
    with open(file_path, 'rb') as file:
        tags = exifread.process_file(file, details=False)
        date_str = tags.get('EXIF DateTimeOriginal')
        return datetime.strptime(str(date_str), '%Y:%m:%d %H:%M:%S') if date_str else None

def count_images(src_folder):
    image_count = 0

    for file in os.listdir(src_folder):
        if file.lower().endswith('.dng') or file.lower().endswith('.jpg'):
            image_count += 1

    return image_count


def get_folder_image_count(src_folder):
    folder_image_count = {}
    
    for root, dirs, files in os.walk(src_folder):
        count = sum(1 for file in files if file.lower().endswith('.dng') or file.lower().endswith('.jpg'))
        folder_image_count[root] = count

    return folder_image_count

def organise_image_files(src_folder, dest_folder):
    files_moved_count = 0
    moved_files = set()

    folder_image_count = get_folder_image_count(src_folder)

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

                        # Check for Esc key press to cancel the operation
                        if keyboard.is_pressed('esc'):
                            print("Operation cancelled by user.")
                            return files_moved_count

    print("\nSummary:")
    for folder, count in folder_image_count.items():
        print(f"{folder}: {count} images")

    return files_moved_count

if __name__ == "__main__":
    
    # Get source folder based on the hostname
    src_folder = get_folders()

    # Count the number of images
    image_count = count_images(src_folder)
    print(f"Found {image_count} images to move.")

    # Ask the user for confirmation
    confirmation = input("Do you want to proceed with organizing? (yes/no): ").lower()

    if confirmation == 'yes':
        dest_folder = get_folders()
        if src_folder and dest_folder:
            # Combine the source folder with the additional folders in a tuple
            all_folders = (src_folder,)

            # Organise images in all selected folders
            for folder in all_folders:
                print(f"\nOrganising DNG and JPG files in {folder}...")
                total_files_moved = organise_image_files(folder, dest_folder)
                print(f"Organising complete. {total_files_moved} files moved.")
        else:
            print("Source or destination folder not selected.")
    else:
        print("Operation cancelled by user.")
