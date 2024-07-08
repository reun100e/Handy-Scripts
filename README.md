# Handy-Scripts
Scripts for simple tasks which saves your ass when you got to do it 1000 times over. 

Please read the code and use with caution. You are liable for any damages from using this code.

## Use case: Media management

### 1. Creating a folder for every file in it
Lets say you have your movie collection. You want to create a folder for each movie and rename it to respective movie name. 

![image](https://github.com/reun100e/Handy-Scripts/assets/47780896/995ec201-a857-4021-ae8e-80f49478e5ea)


Running this script will trake care of it
```
python create_folder_for_every_file.py
```

This script also moves any file with same name into the corresponding folder. In the scenario given above, I needed to move the subtitle file along with the movie.

### 2. Checking if folders contain video & subtitle files

Now lets say you needed to check if all folders contain a .mp4 file. Then use this script:
```
python check_folders_for_mp4.py
```
Or use this script which is the same script in stroids. It checks for all video and subtitle files, and exports a txt file with results. Extremely useful when you got huge data to work with.
```
python check_folders_for_videos_and_subtitles.py
```

![image](https://github.com/reun100e/Handy-Scripts/assets/47780896/33a56fec-461a-4510-9af8-0255d6d803df)

### 3. Comparing two directories for same or similar folders

Now lets say you want to compare if two folders contain the same sub folders. The use this script:
```
python find_same_foldername.py
```
![image](https://github.com/reun100e/Handy-Scripts/assets/47780896/5c79f158-afcb-4551-9fcc-b6e2c5108f5a)

Or use this script which gives similar results. This is extremely useful when there might be a typo or different case usage for similar content.
```
python find_similarity_foldername.py
```

![image](https://github.com/reun100e/Handy-Scripts/assets/47780896/24edc035-c87d-4cf7-944a-e0118e625e45)

### 4. Sort photos and videos in to separate folders by date

Now lets say you have imported all photos from phone or camera and everything is in one single folder or you have nested folders of the same. You want to sort all your photos and videos in to separate folders based on date taken. This script helps you accomplish exactly that:

```
python sort_media_by_date_taken.py <your media folder directory>
```
You can add custom extensions to this script by modifying the config.json file.

## Pre-requisites

1. Install Python and set it up
2. Install libraries used in each respective script. If you dont have it installed, the error will say which package is missing. You just need to install that using pip or other package managers.
```
pip install tqdm
pip install pymediainfo
```
3. Enjoy~

# Contact
Dr. Aghosh B Prasad <br>
aghoshbprasad100@gmail.com
