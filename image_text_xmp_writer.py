"""
A script to pair image and text files and write the text data to the image's XMP metadata.

Usage:
------
1. Run the script.
2. Enter the directory path to search for pairs of image and text files.
3. The script will read each pair of files and write the text data to the image's XMP metadata.
- The text data is written to the 'dc:subject' field in the XMP metadata.
  - If the field already exists, the script will overwrite it.
- The script will print a message for each successful operation or error.
  - If an error occurs, the script will continue processing the remaining pairs.

Build:
------
1. Update PyInstaller:
  pip install --upgrade pyinstaller

2. Build the script:
  pyinstaller --onefile --add-binary "venv\Lib\site-packages\pyexiv2\lib;pyexiv2/lib" script.py

"""


import os
import pyexiv2


def display_help():
    """Display detailed information about the process and tips."""
    print("""
    This script pairs image and text files in a directory and writes the text data to the image's XMP metadata.

    Usage:
    ------
    0. Make backups of your files before running the script.
    1. Place your image files and corresponding text files in the same directory.
       - Ensure that each image file has a corresponding text file with the same base name.
         For example: 'image1.jpg' and 'image1.txt'.
    2. Run the script.
    3. When prompted, enter the directory path containing your files.
       - You can type 'help' or '?' at the prompt to display this information again.

    Tips:
    -----
    - Supported image formats are: .png, .jpg, .jpeg, .tiff
    - The text data from the .txt files will be written to the 'dc:subject' field in the XMP metadata of the images.
    - Existing metadata in the 'dc:subject' field will be overwritten.
    - If you encounter permission errors, try running the script with administrative privileges.
    """)


def get_directory():
    """Prompt the user to enter a directory path and validate its existence.

    Returns:
        str | None: The validated directory path, or None if invalid.
    """
    while True:
        directory = input("Input Path: ").strip()
        if directory.lower() in ('help', '?'):
            display_help()
            continue
        if not os.path.exists(directory):
            print(f"Directory '{directory}' does not exist. Please try again.")
            continue
        return directory


def get_image_text_pairs(directory):
    """Find pairs of image and text files in the directory with the same name.

    Args:
        directory (str): The directory path to search.

    Returns:
        list: A list of tuples containing the image and text file paths.
    """
    images = {}
    text_files = {}
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext in ['.png', '.jpg', '.jpeg', '.tiff']:
            images[name] = os.path.join(directory, filename)
        elif ext == '.txt':
            text_files[name] = os.path.join(directory, filename)
    pairs = [(images[name], text_files[name]) for name in images if name in text_files]
    return pairs


def write_xmp_metadata(image_path, text_path, text_data):
    """Write the text data to the image's XMP metadata (dc:subject field).

    Args:
        image_path (str): The path to the image file.
        text_data (str): The text data to write to the metadata.
    """
    try:
        with pyexiv2.Image(image_path) as img:
            metadata = img.read_xmp()
            metadata['Xmp.dc.subject'] = text_data.splitlines()
            img.modify_xmp(metadata)
        print(f"Success - {os.path.basename(text_path)} to > {os.path.basename(image_path)}")
    except Exception as e:
        print(f"Failed to write metadata to '{image_path}': {e}")


def process_pairs(directory, pairs):
    """Process each pair of image and text files and write the text data to the image's XMP metadata."""
    if not directory:
        return
    if not pairs:
        print("No matching pairs of image and text files found in the directory.")
        return
    total_pairs = len(pairs)
    successes = 0
    failures = 0
    for image_path, text_path in pairs:
        try:
            with open(text_path, 'r', encoding='utf-8') as text_file:
                text_data = text_file.read().strip()
                write_xmp_metadata(image_path, text_path, text_data)
                successes += 1
        except Exception as e:
            print(f"Error reading '{text_path}': {e}")
            failures += 1
    print(f"Done!\nTotal pairs: {total_pairs}, Successfully processed: {successes}, Failed to process: {failures}")


def main():
    """Main function to execute the script."""
    print("Enter the directory to process image-text pairs.\nType 'help' or '?' for more information.\n\n")
    directory = get_directory()
    pairs = get_image_text_pairs(directory)
    process_pairs(directory, pairs)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        input("Press Enter to exit...")
