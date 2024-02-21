import os
import zipfile
import tarfile
import rarfile
from datetime import datetime
import argparse
import json
import PyPDF2
from PIL import Image
import concurrent.futures
import pytesseract
from moviepy.editor import AudioFileClip
import speech_recognition
from textblob import TextBlob
import textract
import nltk
import platform
from pydub import AudioSegment
import subprocess

# Download nltk data for text analysis (you can further customize this based on your needs)
nltk.download('punkt')

class ArchiveMetadataExtractor:
    SUPPORTED_EXTENSIONS = ['.zip', '.tar', '.rar', '.pdf', '.jpg', '.png', '.jpeg', '.txt', '.mp3', '.mp4']

    def __init__(self, file_path):
        self.file_path = file_path
        self.metadata = {}

    def extract_metadata(self, selected_files=None, filter_types=None, extract_content=False, advanced_analysis=False):
        _, file_extension = os.path.splitext(self.file_path)

        if file_extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file format: {file_extension}")

        extraction_methods = {
            '.zip': self.extract_zip_metadata,
            '.tar': self.extract_tar_metadata,
            '.rar': self.extract_rar_metadata,
            '.pdf': self.extract_pdf_metadata,
            '.jpg': self.extract_image_metadata,
            '.png': self.extract_image_metadata,
            '.jpeg': self.extract_image_metadata,
            '.txt': self.extract_text_metadata,
            '.mp3': self.extract_audio_metadata,
            '.mp4': self.extract_video_metadata,
        }

        extraction_methods[file_extension](selected_files, filter_types, extract_content, advanced_analysis)
        self.identify_file_type()

    def _extract_metadata_from_archive(self, archive, selected_files=None, filter_types=None, extract_content=False, advanced_analysis=False):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self._extract_metadata, info, selected_files, filter_types, extract_content, advanced_analysis): info for info in archive.infolist()}
            concurrent.futures.wait(futures)

    def _extract_metadata(self, info, selected_files=None, filter_types=None, extract_content=False, advanced_analysis=False):
        if not selected_files or info.filename in selected_files:
            file_type = self.identify_file_type(info.filename)
            if filter_types and file_type not in filter_types:
                return

            if file_type not in self.metadata:
                self.metadata[file_type] = {}

            self.metadata[file_type][info.filename] = self.get_common_metadata(info)
            if hasattr(info, 'compress_type'):
                self.metadata[file_type][info.filename]['compression_type'] = info.compress_type

            # Call specific extraction method based on file type
            extraction_method = getattr(self, f'extract_{file_type.lower()}_metadata', None)
            if extraction_method:
                extraction_method(info.filename)

            if extract_content:
                self.extract_content(info.filename, file_type)

                if advanced_analysis:
                    self.perform_advanced_analysis(info.filename, file_type)

    def create_clean_zip(self):
        clean_zip_path = self.file_path.replace('.zip', '_clean.zip')
        if platform.system() == 'Windows':
            import shutil
            shutil.make_archive(clean_zip_path[:-4], 'zip', self.file_path)
        else:
            os.system(f'ditto -c -k --sequesterRsrc --keepParent "{self.file_path}" "{clean_zip_path}"')
        return clean_zip_path

    def extract_zip_metadata(self, selected_files=None, filter_types=None, extract_content=False, advanced_analysis=False):
        clean_zip_path = self.create_clean_zip()
        with zipfile.ZipFile(clean_zip_path, 'r') as clean_zip:
            self._extract_metadata_from_archive(clean_zip, selected_files, filter_types, extract_content, advanced_analysis)
        os.remove(clean_zip_path)

    def extract_tar_metadata(self, selected_files=None, filter_types=None, extract_content=False, advanced_analysis=False):
        with tarfile.open(self.file_path, 'r') as tar_file:
            self._extract_metadata_from_archive(tar_file, selected_files, filter_types, extract_content, advanced_analysis)

    def extract_rar_metadata(self, selected_files=None, filter_types=None, extract_content=False, advanced_analysis=False):
        with rarfile.RarFile(self.file_path, 'r') as rar_file:
            self._extract_metadata_from_archive(rar_file, selected_files, filter_types, extract_content, advanced_analysis)

    def extract_pdf_metadata(self, file_name):
        with open(file_name, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            info = pdf_reader.getDocumentInfo()
            self.metadata['PDF_Metadata'] = {
                'title': info.title,
                'author': info.author,
                'subject': info.subject,
                'producer': info.producer,
                'created_date': info.created.strftime('%Y-%m-%d %H:%M:%S UTC'),
                'modified_date': info.modified.strftime('%Y-%m-%d %H:%M:%S UTC'),
                'number_of_pages': len(pdf_reader.pages)
            }

    def extract_image_metadata(self, file_name):
        img = Image.open(file_name)
        self.metadata['Image_Metadata'] = {
            'format': img.format,
            'mode': img.mode,
            'size': img.size,
            'info': img.info
        }

    def extract_text_metadata(self, file_name):
        try:
            # Using pdftotext command-line tool to extract text from PDF
            text_content = subprocess.check_output(['pdftotext', file_name, '-'], universal_newlines=True)
            self.metadata['Text_Metadata'] = {
                'content': text_content
            }
        except Exception as e:
            print(f"Error extracting text content: {str(e)}")

    def extract_audio_metadata(self, file_name):
        audio = AudioSegment.from_file(file_name)
        self.metadata['Audio_Metadata'] = {
            'channels': audio.channels,
            'frame_rate': audio.frame_rate,
            'frame_width': audio.frame_width,
            'frame_count': len(audio),
            'duration_seconds': audio.duration_seconds
        }

    def extract_video_metadata(self, file_name):
        video = AudioFileClip(file_name)
        self.metadata['Video_Metadata'] = {
            'duration': video.duration,
            'fps': video.fps,
            'size': video.size
        }

    def extract_content(self, file_name, file_type):
        # Perform content extraction based on file type
        if file_type.lower() == 'pdf':
            self.extract_pdf_content(file_name)
        elif file_type.lower() == 'image':
            self.extract_image_text_content(file_name)
        elif file_type.lower() == 'audio':
            self.extract_audio_text_content(file_name)
        elif file_type.lower() == 'text':
            self.extract_text_content(file_name)

    def extract_pdf_content(self, file_name):
        with open(file_name, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_content = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text()
            self.metadata['PDF_Content'] = {
                'text_content': text_content
            }

    def extract_image_text_content(self, file_name):
        img = Image.open(file_name)
        text_content = pytesseract.image_to_string(img)
        self.metadata['Image_Content'] = {
            'text_content': text_content
        }

    def extract_audio_text_content(self, file_name):
        recognizer = speech_recognition.Recognizer()
        with speech_recognition.AudioFile(file_name) as audio_file:
            audio_content = recognizer.record(audio_file)
            text_content = recognizer.recognize_google(audio_content)
            self.metadata['Audio_Content'] = {
                'text_content': text_content
            }

    def perform_advanced_analysis(self, file_name, file_type):
        if file_type.lower() in ['pdf', 'image', 'audio', 'text']:
            content_key = f'{file_type.capitalize()}_Content'
            if content_key in self.metadata:
                text_content = self.metadata[content_key]['text_content']
                analysis = self.analyze_text_sentiment(text_content)
                self.metadata[content_key]['Advanced_Analysis'] = {
                    'sentiment': analysis
                }

    def analyze_text_sentiment(self, text_content):
        analysis = TextBlob(text_content)
        return {
            'polarity': analysis.sentiment.polarity,
            'subjectivity': analysis.sentiment.subjectivity
        }

    @staticmethod
    def get_common_metadata(info):
        return {
            'file_size': info.size,
            'compression_type': None,
            'last_modified': datetime.utcfromtimestamp(info.mtime).strftime('%Y-%m-%d %H:%M:%S UTC')
        }

    def identify_file_type(self, filename=None):
        if not filename:
            filename = self.file_path

        _, file_extension = os.path.splitext(filename.lower())

        if file_extension in ['.zip', '.tar', '.rar']:
            return 'Archive'
        elif file_extension in ['.pdf']:
            return 'PDF'
        elif file_extension in ['.jpg', '.png', '.jpeg']:
            return 'Image'
        elif file_extension in ['.txt']:
            return 'Text'
        elif file_extension in ['.mp3']:
            return 'Audio'
        elif file_extension in ['.mp4']:
            return 'Video'
        else:
            return 'Unknown'

def display_metadata_summary(metadata):
    print("\nMetadata Summary:")
    print("----------------------------")
    for file_type, files in metadata.items():
        for file_name, details in files.items():
            print(f"{file_type.capitalize()} File: {file_name}")
            print(f"Size: {details['file_size']} bytes")
            print(f"Last Modified: {details['last_modified']}")
            if details.get('compression_type') is not None:
                print(f"Compression Type: {details['compression_type']}")
            print("----------------------------")

def save_metadata_to_json(metadata, output_file='metadata.json'):
    with open(output_file, 'w') as json_file:
        json.dump(metadata, json_file, indent=2)
    print(f"Metadata saved to {output_file}.")

def main():
    parser = argparse.ArgumentParser(description='Extract metadata from various file formats.')
    parser.add_argument('file_path', help='Path to the file or archive.')
    parser.add_argument('--json', action='store_true', help='Display metadata in JSON format.')
    parser.add_argument('--verbose', action='store_true', help='Display additional details.')
    parser.add_argument('--save-json', metavar='output_file', help='Save metadata to a JSON file.')
    parser.add_argument('--select-files', nargs='+', metavar='file_name',
                        help='Select specific file(s) within an archive to extract metadata.')
    parser.add_argument('--filter-types', nargs='+', metavar='file_type',
                        help='Filter specific file type(s) for extraction.')
    parser.add_argument('--extract-content', action='store_true', help='Extract content from supported files.')
    parser.add_argument('--advanced-analysis', action='store_true', help='Perform advanced analysis on extracted content.')

    args = parser.parse_args()
    file_path = args.file_path

    try:
        metadata_extractor = ArchiveMetadataExtractor(file_path)
        metadata_extractor.extract_metadata(args.select_files, args.filter_types, args.extract_content, args.advanced_analysis)

        if metadata_extractor.metadata:
            if args.verbose:
                print(f"Successfully extracted metadata from {file_path}.")
            display_metadata_summary(metadata_extractor.metadata)
            if args.json:
                print(json.dumps(metadata_extractor.metadata, indent=2))
            if args.save_json:
                save_metadata_to_json(metadata_extractor.metadata, args.save_json)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
