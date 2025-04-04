# PowerPoint to PDF Bulk Converter & PDF Copier (Windows)

This Python script automates the process of converting Microsoft PowerPoint presentations (`.ppt`, `.pptx`) to PDF format in bulk. It recursively scans a specified input directory and its subdirectories. Any PowerPoint files found are converted to PDF in a designated output directory. Existing PDF files found in the input directory are simply copied over to the output directory.

The script utilizes COM automation and requires **Microsoft PowerPoint** to be installed on a **Windows** system.

## Features

*   **Recursive Search:** Scans the specified input folder and all its subfolders for files.
*   **PowerPoint Conversion:** Converts `.ppt` and `.pptx` files to PDF using the Microsoft PowerPoint application for high fidelity.
*   **PDF Copying:** Copies existing `.pdf` files from the input directory structure to the output directory.
*   **Avoids Overwriting:** Checks if a PDF file with the same name already exists in the output directory and skips conversion/copying if it does.
*   **Flat Output Structure:** All resulting PDF files are placed directly into the specified output folder, regardless of their original subfolder location.
*   **Progress Reporting:** Prints status messages to the console during processing.
*   **Summary:** Provides a summary of successful/failed conversions and copies upon completion.
*   **Optimized PowerPoint Usage:** Only starts the PowerPoint application if there are actual `.ppt` or `.pptx` files that need conversion.

## Prerequisites

*   **Operating System:** Windows (XP, Vista, 7, 8, 10, 11)
*   **Software:** Microsoft PowerPoint (Must be installed and functional)
*   **Python:** Python 3.x recommended.
*   **Python Libraries:** `comtypes` and its dependency `pywin32`.

## Setup / Installation

1.  Ensure Python 3.x and Microsoft PowerPoint are installed on your Windows machine.
2.  Open a command prompt (cmd) or PowerShell terminal.
3.  Install the required Python libraries using pip:

    ```bash
    pip install pywin32 comtypes
    ```
    *Note: Depending on your Python installation, you might need to use `python -m pip install ...` or `python3 -m pip install ...`.*

## Configuration

Before running the script, you **must** configure the input and output folder paths:

1.  Open the script file (e.g., `ppt_to_pdf_recursive.py`) in a text editor.
2.  Locate the `Configuration` section near the top of the script.
3.  Modify the `INPUT_FOLDER` variable to the **full path** of the root directory containing your PowerPoint files (and potentially subfolders and PDFs).
4.  Modify the `OUTPUT_FOLDER` variable to the **full path** of the directory where you want the resulting PDF files to be saved.

    ```python
    # --- Configuration ---
    # !!! IMPORTANT: Use raw strings (r"...") or double backslashes (\\) for Windows paths !!!
    INPUT_FOLDER = r"C:\path\to\your\powerpoint_files_root" # The top-level folder to search
    OUTPUT_FOLDER = r"C:\path\to\your\pdf_output"
    # --- End Configuration ---
    ```

    **Important:** Use Windows path conventions:
    *   Raw strings: `r"C:\Users\YourName\Documents"` (Recommended)
    *   Or double backslashes: `"C:\\Users\\YourName\\Documents"`

## Usage

1.  Ensure Microsoft PowerPoint is **closed** before running the script. While the script attempts to run it invisibly, having it closed beforehand is recommended for stability.
2.  Open a command prompt (cmd) or PowerShell terminal.
3.  Navigate (`cd`) to the directory where you saved the Python script.
4.  Run the script using Python:

    ```bash
    python your_script_name.py
    ```
    *(Replace `your_script_name.py` with the actual filename you saved the script as. You might need to use `python3` instead of `python` depending on your system setup).*

5.  The script will start scanning the `INPUT_FOLDER`, process the files, and print progress updates to the console. Converted/copied PDF files will appear in the `OUTPUT_FOLDER`. A final summary will be printed upon completion or error.

## How it Works

The script uses the `comtypes` library to interact with the Microsoft PowerPoint application via its COM (Component Object Model) interface on Windows. It instructs PowerPoint to open each presentation file invisibly, save it as a PDF using PowerPoint's built-in PDF export functionality, and then close the file. For existing PDF files found in the source directory, it uses Python's standard `shutil` module to perform a file copy.

## Important Notes

*   **Windows Only:** This script relies on Windows-specific COM technology and will not work on macOS or Linux.
*   **PowerPoint Required:** Microsoft PowerPoint must be installed; the script does not work without it.
*   **Performance:** Converting many files, especially large or complex presentations, can take a significant amount of time and consume system resources.
*   **Error Handling:** Basic error handling is included. However, heavily corrupted PowerPoint files or unexpected PowerPoint application behavior might cause errors or incomplete conversions. Check the console output for error messages.
*   **Flat Output Structure:** The script does *not* replicate the source folder structure in the output directory. All PDFs are placed directly in the `OUTPUT_FOLDER`.
*   **PowerPoint Interference:** Avoid interacting with the PowerPoint application manually while the script is running.

## License

This script is provided under the GPL-3.0 License. See the LICENSE file in repo root.