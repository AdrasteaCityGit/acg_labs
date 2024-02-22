
ACG_EUGENIA: Archive Metadata Extraction Tool

![alt text](https://www.adrasteagit.com/projects/acg_eugenia/acg_eugenia_logo.png)

acg_eugenia - Comprehensive Image Metadata Extraction Tool
Description
acg_eugenia is a powerful and versatile tool designed for extracting comprehensive metadata from images. This tool supports various functionalities such as displaying detailed metadata information, extracting basic image details, camera information, GPS coordinates, and more. Additionally, it provides advanced features like image rotation, format conversion, thumbnail display, metadata editing, and datetime metadata formatting.
Features
1. Comprehensive Metadata Extraction:
    * Extracts detailed metadata information from images.
2. Basic Image Information:
    * Displays basic image details such as dimensions, color mode, and file size.
3. Camera Information:
    * Extracts camera-related metadata, including make, model, exposure time, aperture, and ISO.
4. GPS Coordinates:
    * Extracts and displays GPS coordinates (latitude, longitude) with a clickable map link.
5. Thumbnail Display:
    * Option to display a thumbnail of the image.
6. Image Rotation:
    * Automatically rotates the image based on its orientation tag.
7. Image Format Conversion:
    * Converts the image to different formats (JPEG, PNG).
8. Display Camera Thumbnail:
    * Displays the thumbnail of the camera (if available in metadata).
9. Metadata Editing:
    * Allows users to edit and update specific metadata fields.
10. Datetime Metadata Formatting:
    * Formats datetime metadata fields for improved readability.
How to Use
1. Installation:
    * Ensure that Python is installed on your system.
    * Install the required libraries using the following command:
    * pip install -r requeriments.txt
    * pip install pillow exifread colorama
    * 
2. Usage:
    * Run the tool with the following command:
    * python acg_eugenia.py <image_path> [options]
    * 
3. Options:
    * --tags: Filter and display specific metadata tags.
    * --thumbnail: Display a thumbnail of the image.
    * --convert_format: Convert image to specified format (JPEG, PNG).
    * --edit_metadata: Edit metadata field with a new value.
    * --format_datetime: Format datetime metadata.
4. Examples:
    * Display comprehensive metadata:
    * python acg_eugenia.py image.jpg
    * 
    * Display thumbnail and convert the image to PNG:
    * python acg_eugenia.py image.jpg --thumbnail --convert_format PNG
    * 
Libraries Used
* Pillow: Python Imaging Library (PIL Fork) for working with images.
* ExifRead: Library for reading Exif metadata from image files.
* Colorama: Library for adding color to terminal text.
OS Compatibility
* The tool is compatible with Windows, macOS, and Linux operating systems.
How it Works
1. The tool extracts metadata using the ExifRead library.
2. Basic image information, camera details, and GPS coordinates are extracted and displayed.
3. Additional functionalities such as image rotation, format conversion, and thumbnail display are implemented.
4. Users can edit specific metadata fields and format datetime metadata.
5. The tool provides a comprehensive report on the image, including clickable map links for GPS coordinates.

