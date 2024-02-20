![alt text](https://www.adrasteagit.com/projects/acg_eugenia/acg_eugenia_logo.png)
ACG_EUGENIA: Archive Metadata Extraction Tool

Overview:
ACG_EUGENIA is a comprehensive command-line utility designed for extracting metadata and content from a diverse range
of file formats. It provides in-depth information about files within an archive, supporting various functionalities
such as metadata extraction, content extraction, trends analysis, graphical user interface (GUI), cloud integration,
customizable output formats, and more.

Functionalities:
1. Metadata Extraction
   - Extracts common metadata including file size, compression type, and last modification date.
   - Supports a wide array of file formats: ZIP, TAR, RAR, PDF, JPG, PNG, JPEG, DOCX, XLSX, PPTX, MP3, MP4, and more.
   - Tailors metadata extraction to each file type for detailed information.

2. Content Extraction
   - Extracts text content from supported file types (PDF, DOCX, PPTX, etc.).
   - Performs advanced text analysis using spaCy.
   - Generates word clouds for a visual representation of text content.

3. Metadata Trends Analysis
   - Analyzes metadata trends such as common file types and average file sizes.
   - Provides statistical summaries for numerical metadata.

4. Graphical User Interface (GUI)
   - Offers a user-friendly GUI powered by tkinter for enhanced accessibility.

5. Cloud Integration
   - Allows users to upload extracted metadata to cloud storage services like AWS S3 or Google Cloud Storage.

6. Customizable Output Formats
   - Supports multiple output formats for metadata, including JSON, CSV, and Excel.

7. Multithreading and Performance Optimization
   - Optimizes performance with multithreading for concurrent file processing within an archive.

8. Language Support
   - Supports multiple languages for text analysis using spaCy or other language processing libraries.

How to Use:
- Prerequisites:
  - Ensure Python (version 3.6 or higher) is installed.
  - Install required dependencies: `pip install -r requirements.txt`

- Command-Line Usage:
  `python acg_eugenia.py <file_path> [options]`
  Options:
  --json: Display metadata in JSON format.
  --verbose: Display additional details.
  --save-json <output_file>: Save metadata to a JSON file.
  --select-files <file_name>: Select specific files within an archive to extract metadata.
  --filter-types <file_type>: Filter metadata extraction to specific file types.
  --extract-content: Extract content (text, etc.) from supported file types.

- GUI Usage:
  Run the tool with the --gui option to launch the graphical user interface.
  `python acg_eugenia.py --gui`

Compatibility:
ACG_EUGENIA is compatible with the following operating systems:
- Windows
- macOS (Mac)
- Linux
Ensure the required dependencies are installed for proper functionality on your operating system.

"ACG_EUGENIA - Metadata Mastery Redefined, Explore the Unseen."
