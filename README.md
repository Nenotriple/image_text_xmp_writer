

# image_text_xmp_writer
A script to pair image and text files and write the text data to the image's XMP metadata.


# 📝 Usage

> [!NOTE]
>
> **Prepare Your Files:**
> - Each image file should have a corresponding text file with the same name.
>   - For example: `01.png`, `01.txt`, `02.jpg`, `02.txt`, etc.
> - Supported image formats: `png`, `jpg`, `jpeg`, `tiff`


### Steps
1. **Run the script.**
2. **Enter the directory path to search for pairs of image and text files.**
3. The script will:
   - Read each pair of files.
   - Write the text data to the image's XMP metadata.
     - The text data is written to the `dc:subject` field in the XMP metadata.
     - If the field already exists, the script will overwrite it.
   - Print a message for each successful operation or error.
     - If an error occurs, the script will continue processing the remaining pairs.


### Tips
- **Make backups before running the script.**
- Supported image formats are: `.png`, `.jpg`, `.jpeg`, `.tiff`.
- The text data from the `.txt` files will be written to the `dc:subject` field in the XMP metadata of the images.
- Existing metadata in the `dc:subject` field will be overwritten.
- If you encounter permission errors, try running the script with administrative privileges.
- You can type `help` or `?` at the prompt to display the help message.


## Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/Nenotriple/image_text_xmp_writer.git
    ```
2. Run `Start.bat` to create a virtual environment and install the required packages.
3. Run `python image_text_xmp_writer.py` to start the script.


## Build
1. **Update PyInstaller:**
    ```bash
    pip install --upgrade pyinstaller
    ```
2. **Build the script:**
    ```bash
    pyinstaller --onefile --add-binary "venv\Lib\site-packages\pyexiv2\lib;pyexiv2/lib" image_text_xmp_writer.py
    ```
