# 2.2 Customized m3u playlist and scheduled guide generation from iptv.org for Jellyfin
If you use m3u streams from [iptv.org](https://github.com/iptv-org/iptv) and wants your own custom m3u playlist as well as generate it's guide.xml using [epg](https://github.com/iptv-org/epg) on a schedule for your [Jellyfin](https://jellyfin.org/) instance, then this is the script for you. I wrote this to use in a windows machine hence powershell. You may use gpt to convert this to your language of choice.

## Initial setup
1. Get all the files from the folder **"2.2. Customized TV playlist and guide from ipvt.org"**.

<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/44327790-2469-4b6a-aa77-0cd0012eaadd" alt="Creation Example" width="500" height="auto">

2. Add the Tv channels you want in **tv.json**. (You can come back to this step again after generating a new list of available channels in available_channels.json)

<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/2f53f117-9320-4340-90ec-af83865ef460" alt="Creation Example" width="auto" height="500">

3. Clone the [iptv.org/epm](https://github.com/iptv-org/epg) repo into the working directory (We will be using this to generate the guide.xml)
```
git clone --depth 1 -b master https://github.com/iptv-org/epg.git
```
Your working directory should look like this:
![image](https://github.com/user-attachments/assets/5a605830-31d5-46fd-aadb-7b024fd55548)


4. Run the 'updateTV.ps1' or schedule it using any means. I personally use Task Scheduler in windows for this.
   - To run the script, Open powershell and cd to project directory and execute the script like this:
```
.\updateTV.ps1
```

5. Once the script finish running, the following files gets updated with latest information from iptv.org
```
./epg/guides.xml
./available_channels.json
./filtered_channels.xml
./filtered_playlist.m3u
./guideXMLTV.xml
```

6. Add the filtered_playlist.m3u and guideXMLTV.xml to your jellyfin Live TV settings.
![image](https://github.com/user-attachments/assets/90632c8f-b9ab-4813-acb7-2ab58030289d)


## Schedule setup
You can schedule to run the updateTV.ps1 any way you like but this is how i did it since i am running this on windows.

1. Open Task Scheduler
   - Windows key + R
   - Type in 'taskschd. msc' and hit Enter
2. Click 'Create Basic Task'
3. Give a name and hit next
4. Specify your schedule
5. Choose 'Start a program' and hit next
6. Fill in these information:
   - Program/script: powershell.exe
   - Add arguments (optional): -NoProfile -ExecutionPolicy Bypass -File "C:\your_path\updateTv.ps1"
   - Start in (optional): C:\your_path
7. Hit Finish
8. You can see the new task created in the list. Right click and properties to change more settings.
9. Right click and click 'run' to test it out.

## Extra reading: Details on what the updateTv.ps1 script does

Here i will explain what the script does in detail step by step.

### 1. Update playlist
The script first downloads the master list of all streams available and creates a new short list of only the channels we need based on the enteries in tv.json. This prevents over crowding of channels in jellyfin. This also makes sure we always get the updated stream links.
- Download https://iptv-org.github.io/iptv/index.m3u
- Updates available_channels.json with tvg-id of all the streams in index.m3u
- Checks tv.json
- Updates filtered_playlist.m3u based on the tvg-id mentioned in tv.json

### 2. Updating channels
We got the stream links, but we also need to get channel guides ([EPG](https://en.wikipedia.org/wiki/Electronic_program_guide)). [iptv.org/epm](https://github.com/iptv-org/epg) can get it for us. But we need to give it the list of channels and from where each channel guide has to be fetched. So the script makes this filtered_channels.xml file next.
- Git pull [iptv.org/epm](https://github.com/iptv-org/epg) repo to get the latest channel guides sources available
- Refers tv.json and searches all the xml files in the repo to create the filtered_channels.xml we need. This is process takes a long time as it searches through all the xml files in the repo to find all the matching sources for the enteries in tv.json
- Updates filtered_channels.xml with the collected information

### 3. Generating guide
Now the script runs the [iptv.org/epm](https://github.com/iptv-org/epg). Since we already pulled the latest git in the previous step, we skip that.
- Installing/updating [iptv.org/epm](https://github.com/iptv-org/epg)
- Runs [iptv.org/epm](https://github.com/iptv-org/epg) with filtered_channels.xml
- [iptv.org/epm](https://github.com/iptv-org/epg) generates guide.xml

### 4. Make guide Jellyfin friendly
This part is something i didn't expect to happen. So basically, the guide.xml made by [iptv.org/epm](https://github.com/iptv-org/epg) doesn't work. I still don't know exactly why but after a lot of trial and error, i realised '&' is used instead  of '&amp' and the encoding was UTF-8 while the [XMLTVFormate](https://wiki.xmltv.org/index.php/XMLTVFormat) sample uses ISO-8859-1. Jellyfin was able to read the guide when these changed were made. So the script does exactly that.
- Takes in guide.xml
- Replaces 'encoding="UTF-8"' with 'encoding="ISO-8859-1"'
- Replaces '(&)(?!amp;|lt;|gt;|quot;|apos;)' with '&amp;'
- Creates a new guideXMLTV.xml with all these changes

# Quality of life features
- A fucntion **Wait-ForInternetConnection** is called everytime just before any operation needing downloading data is concerened. The function basically checks if it gets status code 200 from google.com and if it doesn't, waits 10 seconds and tries again. The function only exits when this condition is met. This assures that the scripts doesnt miss any downloads and waits around till the internet is back.
- **Comments**. The script is filled with comments so modification to any part is easy anyone.

~ Enjoy
