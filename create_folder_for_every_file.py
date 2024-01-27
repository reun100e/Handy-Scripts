import os

def create_folders(directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    # Get the list of files in the directory
    files = os.listdir(directory)

    # Dictionary to store files with the same base name
    file_dict = {}

    # Populate the dictionary
    for file_name in files:
        # Check if the item is a file
        if os.path.isfile(os.path.join(directory, file_name)):
            # Get the file name without extension
            base_name = os.path.splitext(file_name)[0]
            file_path = os.path.join(directory, file_name)

            if base_name in file_dict:
                file_dict[base_name].append(file_path)
            else:
                file_dict[base_name] = [file_path]

    # Create folders based on the dictionary
    for base_name, file_paths in file_dict.items():
        if len(file_paths) == 1:
            # If only one file with this base name, create a folder for it
            folder_path = os.path.join(directory, base_name)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Created folder '{base_name}'")
            os.rename(file_paths[0], os.path.join(folder_path, os.path.basename(file_paths[0])))
        else:
            # If multiple files with this base name, create a folder and move files into it
            folder_path = os.path.join(directory, base_name)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Created folder '{base_name}'")
            for file_path in file_paths:
                os.rename(file_path, os.path.join(folder_path, os.path.basename(file_path)))

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    create_folders(directory)
