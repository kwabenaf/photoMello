import os
import shutil
from datetime import datetime
import exifread

def get_original_date(file_path):
    with open(file_path, 'rb') as file:
        tags = exifread.process_file(file, details=False)
        date_str = tags.get('EXIF DateTimeOriginal')
        if date_str:
            return datetime.strptime(str(date_str), '%Y:%m:%d %H:%M:%S')
        return None

def organize_dng_files(src_folder):
    files_moved_count = 0
    moved_files = set()
    dest_folder = src_folder  # Set dest_folder to the same as src_folder

    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.lower().endswith('.dng'):
                file_path = os.path.join(root, file)
                if file_path not in moved_files:  # Check if the file has already been moved
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
    src_folder = r'D:\ricoh\all'

    print("organising dng files...")
    print("organising complete. all files moved.")
