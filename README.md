# Handy-Scripts
Scripts for simple tasks which saves your ass when you got to do it 1000 times over. 

Please read the code and use with caution. You are liable for any damages from using this code.

[[_TOC_]]

## 1. Multi Media management


| Section | Subsection | Description | Command |
|---------|-------------|-------------|---------|
| **1. Multi Media Management** | **1.1 Creating a Folder for Every File** | Create a folder for each file and rename it to the respective movie name. | `python create_folder_for_every_file.py` |
|  | **1.2 Checking if Folders Contain Video & Subtitle Files** | Check if all folders contain a .mp4 file or other video and subtitle files, and export results. | `python check_folders_for_mp4.py`<br>`python check_folders_for_videos_and_subtitles.py` |
|  | **1.3 Comparing Two Directories for Same or Similar Folders** | Compare if two folders contain the same or similar subfolders. | `python find_same_foldername.py`<br>`python find_similarity_foldername.py` |
|  | **1.4 Preview Webcameras Available on Your Computer** | Preview and choose all available cameras on your PC. | `python camera_preview.py` |
|  | **1.5 Sort Photos and Videos into Separate Folders by Date** | Sort photos and videos into separate folders based on the date taken. | `python sort_media_by_date_taken.py <your media folder directory>` |
| **2. Jellyfin Helpers** | **2.1 Cast Photos Not Appearing in Jellyfin** | Visits all the cast pages in your Jellyfin to ensure cast photos appear. | `python Jellyfin-repair-cast-not-showing.py` |
|  | **2.2 Customized M3U Playlist and Scheduled Guide Generation from IPTV.org** | Generate a custom M3U playlist and guide.xml from IPTV.org on a schedule. | Instructions: Copy the script provided in the repo. |


### 1.1 Creating a folder for every file in it
Lets say you have your movie collection. You want to create a folder for each movie and rename it to respective movie name.

<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/995ec201-a857-4021-ae8e-80f49478e5ea" alt="Folder Creation Example" width="500" height="auto">



Running this script will trake care of it
```
python create_folder_for_every_file.py
```

This script also moves any file with same name into the corresponding folder. In the scenario given above, I needed to move the subtitle file along with the movie.

### 1.2 Checking if folders contain video & subtitle files

Now lets say you needed to check if all folders contain a .mp4 file. Then use this script:
```
python check_folders_for_mp4.py
```
Or use this script which is the same script in stroids. It checks for all video and subtitle files, and exports a txt file with results. Extremely useful when you got huge data to work with.
```
python check_folders_for_videos_and_subtitles.py
```

<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/33a56fec-461a-4510-9af8-0255d6d803df" alt="Creation Example" width="500" height="auto">


### 1.3 Comparing two directories for same or similar folders

Now lets say you want to compare if two folders contain the same sub folders. The use this script:
```
python find_same_foldername.py
```
<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/5c79f158-afcb-4551-9fcc-b6e2c5108f5a" alt="Creation Example" width="500" height="auto">

Or use this script which gives similar results. This is extremely useful when there might be a typo or different case usage for similar content.
```
python find_similarity_foldername.py
```

<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/24edc035-c87d-4cf7-944a-e0118e625e45" alt="Creation Example" width="500" height="auto">

### 1.4 Preview webcameras available in your computer

Run this script to preview chose and preview all available cameras in your pc
```
python camera_preview.py
```
<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/a882f7db-98da-47bb-b61f-7eab08518b61" alt="Creation Example" width="500" height="auto">


### 1.5 Sort photos and videos in to separate folders by date

Now lets say you have imported all photos from phone or camera and everything is in one single folder or you have nested folders of the same. You want to sort all your photos and videos in to separate folders based on date taken. This script helps you accomplish exactly that:

```
python sort_media_by_date_taken.py <your media folder directory>
```
<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/a5932346-f5d6-481f-9c25-6d677a8ccfe6" alt="Creation Example" width="500" height="auto">

You can add custom extensions to this script by modifying the config.json file.

<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/a3e6be02-80ca-4492-ac89-fe73cee5c466" alt="Creation Example" width="500" height="auto">


## Jellyfin helpers
### 2.1 Cast photos not appearing in Jellyfin
In Jellyfin, sometimes the cast photo doesn't show unless the cast page is visited once. This script visits all the cast pages in you Jellyfin so that you don't have to spend another month clicking every cast image. Setup an API from Jellyfin admin settings, give it to the script, and point it to server url - the script will do its job. The script is not mine. It's from [here](https://github.com/jellyfin/jellyfin/issues/8103). This is temporary fix and the issue will likely be fixed in future versions.

![image](https://github.com/user-attachments/assets/c03627b2-30fb-40c4-9e90-edfbf5ca9797)

```
python Jellyfin-repair-cast-not-showing.py
```

### 2.2 Customized m3u playlist and scheduled guide generation from iptv.org
If you use m3u streams from [iptv.org](https://github.com/iptv-org/iptv) and wants your own custom m3u playlist as well as generate it's guide.xml using [epg](https://github.com/iptv-org/epg) on a schedule, then this is the script for you. I wrote this to use in a windows machine hence powershell. You may use gpt to convert this to your language of choice.

1. Get all the files "2.2. Customized TV playlist and guide from ipvt.org".

![image](https://github.com/user-attachments/assets/44327790-2469-4b6a-aa77-0cd0012eaadd)

3. Add Tv channels you want in tv.json.

![image](https://github.com/user-attachments/assets/2f53f117-9320-4340-90ec-af83865ef460)

2. You may manualy run the 'updateTV.ps1' manually or schedule it.
4. You can automate the running of 'updateTV.ps1' by running 'updateTV_Scheduler.ps1' a service. Change the path pointing to 'updateTV.ps1' as well as the schedule as needed.

![image](https://github.com/user-attachments/assets/ab01ffb9-cc1c-4af3-bd56-44360cc246aa)

6. Setup 'updateTV_Scheduler.ps1' as a service using [NSSM](https://nssm.cc/).
After downloading NSSM, using cmd, cd to the nssm folder and run this command after updating the path to your scheduler script 'updateTV_Scheduler.ps1': 
```
nssm install updateTv "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" "-NoProfile -WindowStyle Hidden -File C:\path_to\updateTV_Scheduler.ps1"
```
Use this command to edit the service using nssm if needed.
```
nsssm edit updateTv
```

# Pre-requisites

1. Install Python and set it up
2. Install libraries used in each respective script. If you dont have it installed, the error will say which package is missing. You just need to install that using pip or other package managers.
```
pip install tqdm
pip install tkinter
pip install pymediainfo
```
3. Enjoy~

# Contact
Dr. Aghosh B Prasad <br>
aghoshbprasad100@gmail.com
