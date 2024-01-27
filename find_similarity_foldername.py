import os
from fuzzywuzzy import fuzz

def get_folder_names(directory):
    """
    Get a list of folder names in a directory.
    """
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

def find_similar_folders(directory1, directory2, threshold=80):
    """
    Find similar folder names between two directories using fuzzy string matching.
    """
    folder_names1 = get_folder_names(directory1)
    folder_names2 = get_folder_names(directory2)

    similar_folders = []
    for name1 in folder_names1:
        for name2 in folder_names2:
            similarity = fuzz.token_set_ratio(name1, name2)
            if similarity >= threshold:
                similar_folders.append((name1, name2, similarity))

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
        for folder1, folder2, similarity in similar_folders:
            print(f"Similarity: {similarity}% - {folder1} : {folder2}")
    else:
        print("No similar folders found.")

if __name__ == "__main__":
    main()
