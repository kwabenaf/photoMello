import os
import socket

# Function to determine if the script is running on a laptop
def on_laptop():
    hostname = socket.gethostname()
    return 'laptop' in hostname.lower()

# Destination folders based on the environment
DESTINATION_FOLDERS = {
    'pc': r"D:\ricoh\all\sort",
    'laptop': r"G:\Other computers\My computer\ricoh\all\sort"
}

ADDITIONAL_FOLDERS = {
    'pc': [
        r"D:\ricoh\all",
        r"D:\ricoh\archive",
        r"D:\ricoh\print-ready"
    ],
    'laptop': [
        r"G:\Other computers\My computer\ricoh\all",
        r"G:\Other computers\My computer\ricoh\archive",
        r"G:\Other computers\My computer\ricoh\print-ready"
    ]
}

# Select the appropriate destination folder based on the environment
DESTINATION_FOLDER = DESTINATION_FOLDERS['laptop' if on_laptop() else 'pc']
ADDITIONAL_FOLDERS = ADDITIONAL_FOLDERS['laptop' if on_laptop() else 'pc']
