import argparse
import os
from PIL import Image
from PIL.ExifTags import TAGS
import json
import csv
import pandas as pd
import zipfile

def extract_metadata(image_path):
    with Image.open(image_path) as img:
        exif_data = img._getexif()

        if exif_data is not None:
            mapped_exif_data = {TAGS[key]: exif_data[key] for key in exif_data.keys() if key in TAGS and isinstance(exif_data[key], (str, int, bytes))}
            return mapped_exif_data
        else:
            return None

def save_metadata(metadata, output_file, output_format):
    if output_format == "json":
        with open(output_file, 'w') as json_file:
            json.dump(metadata, json_file, indent=4)
    elif output_format == "csv":
        with open(output_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Tag", "Value"])
            for key, value in metadata.items():
                writer.writerow([key, value])
    elif output_format == "excel":
        df = pd.DataFrame(list(metadata.items()), columns=["Tag", "Value"])
        df.to_excel(output_file, index=False)
    else:
        print(f"Unsupported output format: {output_format}")

def process_image(image_path, output_folder, output_format, archive_name):
    filename = os.path.basename(image_path)
    metadata = extract_metadata(image_path)

    if metadata:
        output_file = os.path.join(output_folder, f"{archive_name}_metadata.{output_format}")
        save_metadata(metadata, output_file, output_format)
    else:
        print(f"No metadata found for {filename}")

def create_archive(output_folder, archive_name):
    archive_path = os.path.join(output_folder, f"{archive_name}.zip")

    with zipfile.ZipFile(archive_path, 'w') as zipf:
        for root, dirs, files in os.walk(output_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, output_folder))

    print(f"Archive created: {archive_path}")

def parse_args():
    parser = argparse.ArgumentParser(description="Process an image and extract metadata.")
    parser.add_argument("image", type=str, help="Path to the input image.")
    parser.add_argument("--output_folder", type=str, default=".", help="Path to the output folder for saving metadata files.")
    parser.add_argument("--output_format", type=str, default="json", choices=["json", "csv", "excel"], help="Output format (json, csv, excel).")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    image_path = args.image
    output_folder = args.output_folder
    output_format = args.output_format.lower()
    archive_name = os.path.splitext(os.path.basename(image_path))[0]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_image(image_path, output_folder, output_format, archive_name)
    create_archive(output_folder, archive_name)
