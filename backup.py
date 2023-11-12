import os
import shutil
import keyboard

# Flag to indicate whether to cancel the operation
cancel_operation = False

# Function to listen for the "ESC" key press
def check_for_cancel(e):
    global cancel_operation
    if e.name == 'esc':
        print("Operation canceled.")
        cancel_operation = True
        keyboard.unhook(check_for_cancel)

def copy_file(source_path, destination_path):
    shutil.copy(source_path, destination_path)

def main():
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
        r"D:\Users\kwabe\Pictures\ricoh\100RICOH",
        r"D:\Users\kwabe\Pictures\ricoh\100RICOH - unfiltered",
        r"D:\Users\kwabe\Pictures\ricoh\100RICOH\1st collection",
        r"D:\Users\kwabe\Pictures\ricoh\100RICOH - unfiltered\1st - edition"
    ]

    # Check if the additional folders exist
    for folder in additional_folders:
        if not os.path.exists(folder):
            print(f"Folder '{folder}' does not exist.")
            return

    copied_files_count = 0  # Initialize the count of copied files
    duplicate_count = 0  # Initialize the count of duplicate files

    # Get a set of files in all additional folders
    additional_files = set()
    for folder in additional_folders:
        additional_files.update(os.listdir(folder))

    # Get a set of files in the destination folder
    destination_files = set(os.listdir(destination_folder))

    # Iterate through files in the source folder
    for filename in os.listdir(source_folder):
        if filename.lower().endswith('.dng') and not cancel_operation:
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(destination_folder, filename)

            # Check if the file already exists in the other folders
            if filename in destination_files or filename in additional_files:
                duplicate_count += 1  # Increment the duplicate count
            else:
                # Copy the .DNG file to the destination folder
                copy_file(source_path, destination_path)
                copied_files_count += 1  # Increment the copied files count

    if not cancel_operation:
        print("Operation complete.")
        print(f"{copied_files_count} .DNG files copied to the destination folder.")
        print(f"{duplicate_count} .DNG files are duplicates.")

if __name__ == "__main__":
    main()
