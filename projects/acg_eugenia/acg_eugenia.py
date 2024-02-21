import argparse
import os
from PIL import Image, ExifTags

def extract_metadata(image_path):
    with Image.open(image_path) as img:
        exif_data = img._getexif()

        if exif_data in not None:
            mapped_exif_data = {ExifTags.TAGS[key]: exif_data[key] for key in exif_data.keys() if key in ExifTags.TAGS}
            return mapped_exif_data
        else: 
            return None

def main():
    parser = argparse.ArgumentParser(description="Extract EXIF metadata from an image.")
    parser.add_argument("image", type=str, help="Path to the input image.")
    args = parser.parse_args()

    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        return

    metadata = extract_metadata(image_path)

    if metadata:
        for key, value in metadata.items():
            print(f"{key}: {value}")
    else:
        print(f"No metadata found for {image_path}")

if __name__ = "main":
    main()