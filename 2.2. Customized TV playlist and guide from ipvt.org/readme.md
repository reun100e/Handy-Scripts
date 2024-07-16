# 2.2 Customized m3u playlist and scheduled guide generation from iptv.org for Jellyfin
If you use m3u streams from [iptv.org](https://github.com/iptv-org/iptv) and wants your own custom m3u playlist as well as generate it's guide.xml using [epg](https://github.com/iptv-org/epg) on a schedule for your [Jellyfin](https://jellyfin.org/) instance, then this is the script for you. I wrote this to use in a windows machine hence powershell. You may use gpt to convert this to your language of choice.

## Initial setup
1. Get all the files from "2.2. Customized TV playlist and guide from ipvt.org".

<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/44327790-2469-4b6a-aa77-0cd0012eaadd" alt="Creation Example" width="500" height="auto">

2. Add the Tv channels you want in tv.json. (You can come back to this step again after generating a new list of available channels in available_channels.json)

<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/2f53f117-9320-4340-90ec-af83865ef460" alt="Creation Example" width="auto" height="500">

3. Clone the iptv.org/epm repo into the working directory (We will be using this to generate the guide.xml)
```
git clone --depth 1 -b master https://github.com/iptv-org/epg.git
```

4. Run the 'updateTV.ps1' or schedule it using any means. I personally use Task Scheduler in windows for this.
Open powershell and cd to project directory
```
.\updateTV.ps1
```

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


