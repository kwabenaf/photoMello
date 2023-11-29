import os

def create_template_structure(root_folder):
    folders = [
        'all', 'archive/Year1', 'archive/Year2',
        'events/Event1', 'events/Event2',
        'themes/Theme1', 'themes/Theme2',
        'printed/.jpg',
        'code', 'print-ready/.jpg',
        'cloud-backup/GoogleDrive/all', 'cloud-backup/GoogleDrive/archive/Year1',
        'cloud-backup/GoogleDrive/archive/Year2', 'cloud-backup/GoogleDrive/events/Event1',
        'cloud-backup/GoogleDrive/events/Event2', 'cloud-backup/GoogleDrive/themes/Theme1',
        'cloud-backup/GoogleDrive/themes/Theme2'
    ]

    root_path = os.path.join(os.getcwd(), root_folder)

    for folder in folders:
        folder_path = os.path.join(root_path, folder)
        os.makedirs(folder_path, exist_ok=True)

if __name__ == "__main__":
    root_folder_name = input("Enter the root folder name: ")
    create_template_structure(root_folder_name)
