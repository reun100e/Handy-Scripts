import os
from mutagen.mp3 import MP3


def list_mp3_files_with_length(folder_path):
    # Iterate through the files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".mp3"):
            file_path = os.path.join(folder_path, file_name)
            audio = MP3(file_path)
            length = audio.info.length
            # Convert length from seconds to minutes and seconds
            minutes, seconds = divmod(length, 60)

            # Remove the file extension and split the name into components
            name_without_extension = os.path.splitext(file_name)[0]
            parts = name_without_extension.split(" - ")

            # Reformat from "78 - Lizzo - Boys.mp3" to "78 - Boys - Lizzo - {minutes}:{seconds}"
            if len(parts) == 3:
                track_number = parts[0]
                artist = parts[1]
                song_title = parts[2]
                formatted_name = f"{track_number} - {song_title} - {artist} - {int(minutes)}:{int(seconds):02d}"
                print(formatted_name)


# Replace 'your/folder/path' with the path to your folder
folder_path = "your/folder/path"
list_mp3_files_with_length(folder_path)
