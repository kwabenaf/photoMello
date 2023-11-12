import os
import shutil
import keyboard

# Flag to indicate whether to cancel the operation
cancel_operation = False

# Counter for the number of files copied
copied_files_count = 0

# Function to listen for the "ESC" key press
def check_for_cancel(e):
    global cancel_operation
    if e.name == 'esc':
        print("Operation canceled.")
        cancel_operation = True
        keyboard.unhook(check_for_cancel)

def copy_file(source_path, destination_path):
    global copied_files_count
    shutil.copy(source_path, destination_path)
    copied_files_count += 1

def process_folder(source_folder, destination_folder, additional_folders):
    global cancel_operation

    # Get a set of files in all additional folders
    additional_files = set()
    for folder in additional_folders:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                additional_files.update(files)

    # Get a set of files in the destination folder
    destination_files = set(os.listdir(destination_folder))

    # Iterate through files in the source folder and its subdirectories
    for root, dirs, files in os.walk(source_folder):
        for filename in files:
            if filename.lower().endswith('.dng') and not cancel_operation:
                source_path = os.path.join(root, filename)
                destination_path = os.path.join(destination_folder, filename)

                # Check if the file already exists in the other folders
                if filename in destination_files or filename in additional_files:
                    print(f"Skipping duplicate file: {filename}")
                else:
                    # Copy the .DNG file to the destination folder
                    copy_file(source_path, destination_path)
                    print(f"File copied: {filename}")

def main():
    global copied_files_count

    # Listen for the "ESC" key press to cancel the operation
    keyboard.on_press_key('esc', check_for_cancel)

    # Ask the user for the source folder
    source_folder = input("Enter the source folder path: ")

    # Check if the source folder exists
    if not os.path.exists(source_folder):
        print("Source folder does not exist.")
        return

    # Specify the destination folder
    destination_folder = r"D:\Users\kwabe\Pictures\ricoh\100RICOH - unfiltered\new"

    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Specify the paths of the additional folders to check for duplicates
    additional_folders = [
        r"D:\Users\kwabe\Pictures\ricoh\100RICOH"
    ]

    # Check if the additional folders exist
    for folder in additional_folders:
        if not os.path.exists(folder):
            print(f"Folder '{folder}' does not exist.")
            return

    # Process the source folder and its subdirectories
    process_folder(source_folder, destination_folder, additional_folders)

    if not cancel_operation:
        print("Operation complete.")
        print(f"{copied_files_count} .DNG files copied to the destination folder.")

if __name__ == "__main__":
    main()
