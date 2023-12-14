from PIL import Image
import os
#import shutil

def convert_dng_to_jpg(root_folder, destination_folder):
    for subdir, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file.lower().endswith(".dng"):
                convert_and_save(file_path, destination_folder)

def convert_and_save(dng_file, destination_folder):
    try:
        with Image.open(dng_file) as img:
            jpg_file = os.path.join(destination_folder, os.path.basename(dng_file))
            jpg_file = os.path.splitext(jpg_file)[0] + ".jpg"
            img.convert("RGB").save(jpg_file, "JPEG")
            print(f"Converted: {dng_file} -> {jpg_file}")
    except Exception as e:
        print(f"Error converting {dng_file}: {e}")

# Example usage:
root_folder = r"D:\ricoh\print-ready"
destination_folder = r"D:\ricoh\print-ready\.jpg"

# Make sure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

convert_dng_to_jpg(root_folder, destination_folder)
