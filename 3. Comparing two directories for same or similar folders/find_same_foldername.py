import os

def get_folder_names(directory):
    """
    Get a list of folder names in a directory.
    """
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

def find_similar_folders(directory1, directory2):
    """
    Find similar folder names between two directories.
    """
    folder_names1 = set(get_folder_names(directory1))
    folder_names2 = set(get_folder_names(directory2))

    similar_folders = folder_names1.intersection(folder_names2)
    return similar_folders

def main():
    # Provide the paths to the directories you want to compare
    directory1 = r"PATH A"
    directory2 = r"PATH B"

    if not os.path.exists(directory1) or not os.path.exists(directory2):
        print("One or both directories do not exist.")
        return

    similar_folders = find_similar_folders(directory1, directory2)

    if similar_folders:
        print("Similar folders found:")
        for folder in similar_folders:
            print(folder)
    else:
        print("No similar folders found.")

if __name__ == "__main__":
    main()
