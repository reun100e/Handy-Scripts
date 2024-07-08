import os
import shutil
import logging
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from pymediainfo import MediaInfo
import argparse
import json

# Configure logging
logging.basicConfig(
    filename="file_organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_photo_date(file_path):
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == "DateTimeOriginal":
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        logging.error(f"Error reading EXIF data from {file_path}: {e}")
    return None


def get_video_date(file_path):
    try:
        media_info = MediaInfo.parse(file_path)
        for track in media_info.tracks:
            if track.track_type == "General":
                for date_field in [
                    "encoded_date",
                    "tagged_date",
                    "file_creation_date",
                    "file_modification_date",
                ]:
                    date_str = getattr(track, date_field, None)
                    if date_str:
                        try:
                            date_str = date_str.split(" UTC")[0]
                            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            logging.warning(
                                f"Could not parse date {date_str} for {file_path}"
                            )
    except Exception as e:
        logging.error(f"Error reading media info from {file_path}: {e}")
    return None


def handle_duplicate(target_folder, filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(target_folder, new_filename)):
        new_filename = f"{base}_{counter}{extension}"
        counter += 1

    return new_filename


def organize_files_by_date(directory, photo_extensions, video_extensions):
    if not os.path.isdir(directory):
        logging.error(f"Directory {directory} does not exist.")
        return

    logging.info(f"Starting organization in directory {directory}")

    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            if os.path.isfile(file_path):
                file_date = None
                if filename.lower().endswith(tuple(photo_extensions)):
                    file_date = get_photo_date(file_path)
                elif filename.lower().endswith(tuple(video_extensions)):
                    file_date = get_video_date(file_path)

                if file_date:
                    date_folder = file_date.strftime("%Y-%m-%d")
                    target_folder = os.path.join(directory, date_folder)
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)

                    new_filename = handle_duplicate(target_folder, filename)
                    shutil.move(file_path, os.path.join(target_folder, new_filename))
                    logging.info(f"Moved {filename} to {target_folder}/{new_filename}")
                else:
                    logging.warning(f"Could not determine the date for file {filename}")

    logging.info(f"Finished organization in directory {directory}")


def main():
    parser = argparse.ArgumentParser(description="Organize photos and videos by date.")
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the directory containing photos and videos",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="The path to the configuration file",
    )

    args = parser.parse_args()

    with open(args.config, "r") as config_file:
        config = json.load(config_file)

    photo_extensions = config.get("photo_extensions", [])
    video_extensions = config.get("video_extensions", [])

    organize_files_by_date(args.directory, photo_extensions, video_extensions)


if __name__ == "__main__":
    main()
