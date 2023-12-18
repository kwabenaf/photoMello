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

def organize_dng_files(src_folder, dest_folder, target_year, target_month):
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.lower().endswith('.dng'):
                file_path = os.path.join(root, file)
                original_date = get_original_date(file_path)
                if original_date and original_date.year == target_year and original_date.month == target_month:
                    dest_path = os.path.join(dest_folder, str(target_year), f"{target_month:02d}")
                    os.makedirs(dest_path, exist_ok=True)
                    shutil.move(file_path, os.path.join(dest_path, file))

if __name__ == "__main__":
    src_folder = r'G:\Other computers\My computer\ricoh\all\2023'
    dest_folder = r'G:\Other computers\My computer\ricoh\all\2023\10'
    target_year = 2023
    target_month = 10

    organize_dng_files(src_folder, dest_folder, target_year, target_month)
