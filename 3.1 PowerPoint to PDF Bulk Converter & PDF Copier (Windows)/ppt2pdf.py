import os
import sys
import comtypes.client
import time
import shutil

# --- Configuration ---
INPUT_FOLDER = r"C:\path\to\your\powerpoint_files_root" # The top-level folder to search
OUTPUT_FOLDER = r"C:\path\to\your\pdf_output"
# Supported extensions (case-insensitive)
PPT_EXTENSIONS = ('.ppt', '.pptx')
# --- End Configuration ---

# Constants for PowerPoint's SaveAs method
ppSaveAsPDF = 32  # PDF format code

def convert_ppt_to_pdf_win(input_path, output_path, powerpoint_app):
    """Converts a single PowerPoint file to PDF using COM."""
    # Calculate relative path for display - handle potential errors if not relative
    try:
        relative_input_path = os.path.relpath(input_path, INPUT_FOLDER)
    except ValueError:
        relative_input_path = input_path # Fallback to full path if not relative

    try:
        # Use .format() instead of f-string
        print("Opening: {}".format(relative_input_path))
        # Open the presentation without opening a window
        presentation = powerpoint_app.Presentations.Open(
            input_path,
            WithWindow=False, # Run in background
            ReadOnly=True,
            Untitled=False
        )

        # Use .format() instead of f-string
        print("Converting: {} -> {}".format(relative_input_path, os.path.basename(output_path)))
        # Save As PDF
        presentation.SaveAs(output_path, ppSaveAsPDF)

        # Use .format() instead of f-string
        print("Closing: {}".format(relative_input_path))
        presentation.Close()

    except Exception as e:
        # Use .format() instead of f-string
        print("ERROR converting {}: {}".format(relative_input_path, e))
        # Attempt to close presentation if it exists and an error occurred mid-process
        try:
            if 'presentation' in locals() and presentation:
                presentation.Close()
        except Exception as close_e:
             # Use .format() instead of f-string
            print("  Warning: Could not close presentation after error: {}".format(close_e))
        return False # Indicate failure
    return True # Indicate success

def bulk_process_recursive():
    """
    Finds PPT files recursively in INPUT_FOLDER, converts them to PDF in
    OUTPUT_FOLDER. Copies existing PDF files from INPUT_FOLDER to OUTPUT_FOLDER.
    Output structure is flat.
    """
    if not os.path.isdir(INPUT_FOLDER):
        print("ERROR: Input folder not found: {}".format(INPUT_FOLDER))
        return
    if not os.path.isdir(OUTPUT_FOLDER):
        print("Output folder not found, creating: {}".format(OUTPUT_FOLDER))
        os.makedirs(OUTPUT_FOLDER)

    powerpoint = None # Initialize PowerPoint COM object to None
    successful_conversions = 0
    failed_conversions = 0
    successful_copies = 0 # Counter for copied PDFs
    failed_copies = 0     # Counter for failed PDF copies
    skipped_files = 0     # Counter for skipped files (output already exists)
    processed_files = 0   # Counter for total files scanned

    try:
        print("Scanning folder recursively: {}".format(INPUT_FOLDER))
        # Use os.walk to traverse directory tree
        for dirpath, dirnames, filenames in os.walk(INPUT_FOLDER):
            print("\n--- Processing directory: {} ---".format(dirpath))
            for filename in filenames:
                processed_files += 1
                input_file_path = os.path.abspath(os.path.join(dirpath, filename))
                should_print_separator = True # Flag to print separator unless skipped

                # --- Handle PowerPoint Files ---
                if filename.lower().endswith(PPT_EXTENSIONS):
                    base_name = os.path.splitext(filename)[0]
                    output_file_path = os.path.abspath(os.path.join(OUTPUT_FOLDER, "{}.pdf".format(base_name)))

                    if os.path.exists(output_file_path):
                         print("Skipping conversion: Output file already exists - {}".format(os.path.basename(output_file_path)))
                         skipped_files += 1
                         should_print_separator = False # Don't print separator if skipped
                         continue # Move to the next file

                    # --- Start PowerPoint only if needed ---
                    if powerpoint is None:
                        try:
                            print("Starting PowerPoint application (invisible)...")
                            powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
                            # powerpoint.Visible = True # Uncomment for debugging
                            print("PowerPoint application started.")
                        except Exception as start_e:
                            print("FATAL ERROR: Could not start PowerPoint application: {}".format(start_e))
                            # If PowerPoint can't start, we can't convert, so exit.
                            # Set failed_conversions to -1 to indicate major failure.
                            failed_conversions = -1
                            raise start_e # Reraise the exception to stop the script

                    # --- Perform Conversion ---
                    if convert_ppt_to_pdf_win(input_file_path, output_file_path, powerpoint):
                         successful_conversions += 1
                    else:
                         failed_conversions += 1

                # --- Handle Existing PDF Files ---
                elif filename.lower().endswith('.pdf'):
                    output_file_path = os.path.abspath(os.path.join(OUTPUT_FOLDER, filename)) # Keep original filename

                    if os.path.exists(output_file_path):
                        print("Skipping copy: Output file already exists - {}".format(filename))
                        skipped_files += 1
                        should_print_separator = False # Don't print separator if skipped
                        continue # Move to the next file

                    # --- Perform Copy ---
                    print("Copying PDF: {} -> {}".format(filename, os.path.basename(output_file_path)))
                    try:
                        shutil.copy2(input_file_path, output_file_path) # copy2 preserves metadata like modification time
                        successful_copies += 1
                    except Exception as copy_e:
                        print("ERROR copying {}: {}".format(filename, copy_e))
                        failed_copies += 1

                # --- Handle Other File Types ---
                else:
                    # Optional: Log skipped non-ppt/non-pdf files
                    # print("Skipping other file type: {}".format(filename))
                    should_print_separator = False # Don't print separator for ignored files
                    pass # Just ignore other file types silently

                # --- Print Separator ---
                if should_print_separator:
                    print("-" * 20) # Separator between processed files


    except Exception as e:
        # Catch general errors, including the re-raised PowerPoint start error
        if failed_conversions != -1: # Avoid double-printing fatal error message
            print("FATAL ERROR during processing: {}".format(e))
        # Mark as major failure if not already marked by PowerPoint start failure
        if failed_conversions != -1:
             failed_conversions = -1
    finally:
        # Ensure PowerPoint is closed properly ONLY if it was started
        if powerpoint:
            print("\nQuitting PowerPoint application...")
            try:
                powerpoint.Quit()
                # Release COM object might be needed in some complex scenarios,
                # but comtypes often handles it. Explicitly deleting helps.
                del powerpoint
                powerpoint = None # Ensure it's marked as gone
                # Give it a moment to fully shut down if needed
                time.sleep(1)
                print("PowerPoint application quit.")
            except Exception as quit_e:
                print("Warning: Error trying to quit PowerPoint: {}".format(quit_e))

        print("\n--- Processing Summary ---")
        print("Total Files Scanned:     {}".format(processed_files))
        print("--------------------------")
        if failed_conversions != -1: # Avoid printing counts if there was a fatal setup error
            print("PPT > PDF Conversions:")
            print("  Successful:          {}".format(successful_conversions))
            print("  Failed:              {}".format(failed_conversions))
            print("PDF Copies:")
            print("  Successful:          {}".format(successful_copies))
            print("  Failed:              {}".format(failed_copies))
            print("--------------------------")
            print("Skipped (Exists):      {}".format(skipped_files))
        else:
            print("Processing failed to complete due to a fatal error (e.g., cannot start PowerPoint).")
        print("==========================")


if __name__ == "__main__":
    # Check if running on Windows
    if sys.platform != "win32":
        print("This script is designed for Windows with PowerPoint installed.")
        print("Please use a different script for other operating systems.")
    else:
        bulk_process_recursive()