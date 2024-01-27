import os

def check_folders_for_mp4(directory):
    """
    Check if every folder in the given directory contains at least one .mp4 file.
    """
    folders_with_mp4 = set()
    folders_without_mp4 = set()
    
    for root, dirs, files in os.walk(directory):
        if files:
            mp4_files = [file for file in files if file.endswith('.mp4')]
            if mp4_files:
                folders_with_mp4.add(root)
            else:
                folders_without_mp4.add(root)

    if folders_without_mp4:
        print("Folders without .mp4 files:")
        for folder in folders_without_mp4:
            print(folder)
    else:
        print("Every folder contains at least one .mp4 file.")

    if folders_with_mp4:
        print("Folders with .mp4 files:")
        for folder in folders_with_mp4:
            print(folder)
    else:
        print("No folders contain .mp4 files.")

def main():
    # Provide the path to the directory you want to check
    directory = r"\\Reundev\d\Torrents\collection"

    if not os.path.exists(directory):
        print("Directory does not exist.")
        return

    check_folders_for_mp4(directory)

if __name__ == "__main__":
    main()
