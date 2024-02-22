import argparse
import os
import exifread
from PIL import Image, ImageOps
from colorama import Fore, Style
import logging
import io
import datetime

logging.basicConfig(filename='metadata_extraction.log', level=logging.ERROR)

def extract_metadata(image_path):
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
        return tags
    except Exception as e:
        logging.error(f"Error reading metadata for {image_path}: {e}")
        return None

def convert_to_decimal_degrees(rational_list):
    degrees = rational_list[0].num / rational_list[0].den
    minutes = rational_list[1].num / rational_list[1].den
    seconds = rational_list[2].num / rational_list[2].den
    return degrees + (minutes / 60.0) + (seconds / 3600.0)

def generate_map_link(latitude, longitude):
    return f"https://www.google.com/maps/place/{latitude:.12f},{longitude:.12f}"

def save_metadata_to_file(metadata, output_file):
    try:
        with open(output_file, 'w') as file:
            file.write("Comprehensive Metadata:\n")
            for tag, value in metadata.items():
                file.write(f"{tag}: {value}\n")
        print(f"{Fore.GREEN}Metadata saved to: {output_file}{Style.RESET_ALL}")
    except Exception as e:
        logging.error(f"Error saving metadata to file: {e}")

def print_section_heading(heading):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{heading}{Style.RESET_ALL}")

def print_metadata(metadata):
    if metadata:
        print_section_heading("Comprehensive Metadata")
        for tag, value in metadata.items():
            print(f"{Fore.YELLOW}{tag}{Style.RESET_ALL}: {value}")
        return True
    return False

def extract_basic_info(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            color_mode = img.mode
            file_size = os.path.getsize(image_path) / (1024.0**2)  # in MB
            return width, height, color_mode, file_size
    except Exception as e:
        logging.error(f"Error extracting basic information: {e}")
        return None

def extract_camera_info(metadata):
    camera_info = {}
    camera_info['Make'] = metadata.get('Image Make')
    camera_info['Model'] = metadata.get('Image Model')
    camera_info['Exposure Time'] = metadata.get('EXIF ExposureTime')
    camera_info['Aperture'] = metadata.get('EXIF FNumber')
    camera_info['ISO'] = metadata.get('EXIF ISOSpeedRatings')
    return camera_info

def extract_all_tags(metadata):
    return list(metadata.keys())

def print_basic_info(width, height, color_mode, file_size):
    if width and height and color_mode and file_size:
        print_section_heading("Basic Image Information")
        print(f"Dimensions: {width} x {height} pixels")
        print(f"Color Mode: {color_mode}")
        print(f"File Size: {file_size:.2f} MB")
        return True
    return False

def print_camera_info(camera_info):
    if any(camera_info.values()):
        print_section_heading("Camera Information")
        for key, value in camera_info.items():
            if value:
                print(f"{key}: {value}")
        return True
    return False

def print_all_tags(metadata):
    all_tags = extract_all_tags(metadata)
    if all_tags:
        print_section_heading("All Available Tags")
        for tag in all_tags:
            print(tag)
        return True
    return False

def filter_and_print_tags(metadata, tags_to_display):
    filtered_tags = {tag: metadata[tag] for tag in tags_to_display if tag in metadata}
    if filtered_tags:
        print_section_heading("Filtered Tags")
        for tag, value in filtered_tags.items():
            print(f"{tag}: {value}")
        return True
    return False

def display_thumbnail(image_path):
    try:
        with Image.open(image_path) as img:
            thumbnail = ImageOps.exif_transpose(img).thumbnail((100, 100))
            thumbnail.show()
    except Exception as e:
        logging.error(f"Error displaying thumbnail: {e}")

def rotate_image_based_on_orientation(image_path):
    try:
        with Image.open(image_path) as img:
            orientation_tag = img.get('Image Orientation')
            if orientation_tag:
                orientation = orientation_tag.values
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(-90, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)
                img.save(image_path)
    except Exception as e:
        logging.error(f"Error rotating image for {image_path}: {e}")

def convert_image_format(image_path, output_format):
    try:
        with Image.open(image_path) as img:
            output_path = os.path.splitext(image_path)[0] + f'_converted.{output_format.lower()}'
            img.save(output_path)
            print(f"{Fore.GREEN}Image converted to {output_format.upper()}. Saved as: {output_path}{Style.RESET_ALL}")
    except Exception as e:
        logging.error(f"Error converting image format for {image_path}: {e}")

def display_camera_thumbnail(metadata):
    thumbnail_data = metadata.get('EXIF Thumbnail')
    if thumbnail_data:
        try:
            with Image.open(io.BytesIO(thumbnail_data)):
                thumbnail.show()
        except Exception as e:
            logging.error(f"Error displaying camera thumbnail: {e}")

def edit_metadata(metadata, tag_to_edit, new_value):
    try:
        tag_to_edit_upper = tag_to_edit.upper()
        if tag_to_edit_upper in metadata:
            metadata[tag_to_edit_upper] = exifread.classes.IfdTag(tag_to_edit_upper, tag_to_edit_upper, new_value)
            print(f"{Fore.GREEN}Metadata field {tag_to_edit} updated to: {new_value}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error: Metadata field {tag_to_edit} not found.{Style.RESET_ALL}")
    except Exception as e:
        logging.error(f"Error editing metadata field {tag_to_edit}: {e}")

def format_datetime_metadata(metadata, datetime_tags):
    for tag in datetime_tags:
        if tag in metadata:
            raw_value = metadata[tag].values
            try:
                formatted_value = datetime.datetime.strptime(raw_value, '%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                metadata[tag] = exifread.classes.IfdTag(tag, tag, formatted_value)
                print(f"{Fore.GREEN}Metadata field {tag} formatted to: {formatted_value}{Style.RESET_ALL}")
            except ValueError:
                logging.error(f"Error formatting datetime metadata for {tag}: Invalid date/time format.")

def main():
    parser = argparse.ArgumentParser(description="Extract comprehensive metadata from an image.")
    parser.add_argument("image", type=str, help="Path to the input image.")
    parser.add_argument("--tags", nargs='+', help="Filter and display specific metadata tags.")
    parser.add_argument("--thumbnail", action="store_true", help="Display thumbnail of the image.")
    parser.add_argument("--convert_format", type=str, choices=["JPEG", "PNG"], help="Convert image to specified format.")
    parser.add_argument("--edit_metadata", nargs=2, metavar=("tag", "value"), help="Edit metadata field with new value.")
    parser.add_argument("--format_datetime", action="store_true", help="Format datetime metadata.")
    args = parser.parse_args()

    image_path = args.image

    if not os.path.exists(image_path):
        print(f"{Fore.RED}Error: Image file not found: {image_path}{Style.RESET_ALL}")
        return

    metadata = extract_metadata(image_path)

    if print_metadata(metadata):
        # Extract and display basic information
        basic_info = extract_basic_info(image_path)
        print_basic_info(*basic_info)

        # Extract and display camera information
        camera_info = extract_camera_info(metadata)
        print_camera_info(camera_info)

        # Extract GPS information
        gps_latitude = metadata.get('GPS GPSLatitude')
        gps_longitude = metadata.get('GPS GPSLongitude')

        if gps_latitude and gps_longitude:
            latitude = convert_to_decimal_degrees(gps_latitude.values)
            longitude = convert_to_decimal_degrees(gps_longitude.values)

            # Generate map link
            map_link = generate_map_link(latitude, longitude)
            print_section_heading("GPS Coordinates")
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
            print(f"Map Link: {map_link}")

            # Save metadata to a file named eugenia_.txt in the script's directory
            script_directory = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(script_directory, "eugenia_.txt")
            save_metadata_to_file(metadata, output_file)

        # Display all available tags
        print_all_tags(metadata)

        # Filter and display specific tags if provided
        if args.tags:
            filter_and_print_tags(metadata, args.tags)

        # Display thumbnail if requested
        if args.thumbnail:
            display_thumbnail(image_path)

        # Rotate image based on orientation
        rotate_image_based_on_orientation(image_path)

        # Convert image format if specified
        if args.convert_format:
            convert_image_format(image_path, args.convert_format)

        # Display camera thumbnail if available
        display_camera_thumbnail(metadata)

        # Edit metadata if specified
        if args.edit_metadata:
            edit_metadata(metadata, args.edit_metadata[0], args.edit_metadata[1])

        # Format datetime metadata if specified
        if args.format_datetime:
            datetime_tags = ['Image DateTime', 'EXIF DateTimeOriginal', 'EXIF DateTimeDigitized']
            format_datetime_metadata(metadata, datetime_tags)

if __name__ == "__main__":
    main()

