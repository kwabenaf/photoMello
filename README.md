# photoMello App

## Overview
photoMello is a Python application built with Tkinter for efficient photo management. It provides functionalities for importing, organizing, and converting photos.

## Files
1. **photoMello.py**
   - Main application with features for importing, organizing, and converting images.

2. **image_viewer.py**
   - Module for viewing and converting raw images to JPEG using rawpy and Pillow.

3. **organise_photos.py**
   - Module for navigating, saving, and archiving photos in a selected folder.

## Dependencies
- Tkinter
- Pillow
- rawpy
- keyboard

## Install Dependencies
```bash
pip install tk Pillow rawpy keyboard
```

## How to Run
Execute `photoMello.py` to launch the app. Import photos, organize, and convert to JPEG.

## Functionality
- **Import Photos:**
  - Choose a source folder for photo import.
  - Organize photos to a destination folder based on system type.

- **Organize Photos:**
  - Navigate with arrow keys.
  - Save or archive images using arrow keys.

- **Convert to JPEG:**
  - Convert raw (.DNG) images to JPEG.
  - Preview, select output location, and convert.

## Notes
- Adjust white balance parameters for raw image processing.
- Ensure specified folders exist on your system.

## Troubleshooting
Check console for errors. Verify folder existence and permissions.
