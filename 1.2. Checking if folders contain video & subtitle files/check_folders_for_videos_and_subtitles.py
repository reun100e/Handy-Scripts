import os
from tqdm import tqdm

# List of video file extensions
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.mpg', '.3gp']

# List of subtitle file extensions
SUBTITLE_EXTENSIONS = ['.srt', '.sub', '.sbv', '.vtt', '.ass', '.ssa', '.usf', '.idx', '.pjs', '.smi']

def check_folders_for_videos_and_subtitles(directory, export_to_file=False, file_path=None):
    """
    Check if every folder in the given directory contains at least one video file and one subtitle file.
    """
    folders_with_videos = set()
    folders_with_subtitles = set()
    folders_without_videos = set()
    folders_without_subtitles = set()
    
    for root, dirs, files in tqdm(os.walk(directory), desc="Checking folders", unit="folder"):
        if files:
            video_files = [file for file in files if os.path.splitext(file)[1].lower() in VIDEO_EXTENSIONS]
            subtitle_files = [file for file in files if os.path.splitext(file)[1].lower() in SUBTITLE_EXTENSIONS]
            
            if video_files:
                folders_with_videos.add(root)
            else:
                folders_without_videos.add(root)
                
            if subtitle_files:
                folders_with_subtitles.add(root)
            else:
                folders_without_subtitles.add(root)

    if export_to_file:
        export_results(folders_with_videos, folders_with_subtitles, file_path)
    else:
        print_results(folders_with_videos, folders_with_subtitles, folders_without_videos, folders_without_subtitles)

def print_results(folders_with_videos, folders_with_subtitles, folders_without_videos, folders_without_subtitles):
    """
    Print the results to the console.
    """
    if folders_without_videos:
        print("Folders without video files:")
        for folder in folders_without_videos:
            print(folder)
    else:
        print("Every folder contains at least one video file.")

    if folders_without_subtitles:
        print("Folders without subtitle files:")
        for folder in folders_without_subtitles:
            print(folder)
    else:
        print("Every folder contains at least one subtitle file.")

    if folders_with_videos:
        print("Folders with video files:")
        for folder in folders_with_videos:
            print(folder)
    else:
        print("No folders contain video files.")

    if folders_with_subtitles:
        print("Folders with subtitle files:")
        for folder in folders_with_subtitles:
            print(folder)
    else:
        print("No folders contain subtitle files.")

def export_results(folders_with_videos, folders_with_subtitles, file_path):
    """
    Export the results to a text file.
    """
    with open(file_path, 'w') as f:
        f.write("Folders with video files:\n")
        for folder in folders_with_videos:
            f.write(folder + '\n')

        f.write("\nFolders with subtitle files:\n")
        for folder in folders_with_subtitles:
            f.write(folder + '\n')

def main():
    # Provide the path to the directory you want to check
    directory = r"\\Reundev\d\ENTERTAINMENT\MOVIES - English"

    if not os.path.exists(directory):
        print("Directory does not exist.")
        return

    export_to_file = True
    file_path = "check_results.txt"

    check_folders_for_videos_and_subtitles(directory, export_to_file, file_path)

if __name__ == "__main__":
    main()
