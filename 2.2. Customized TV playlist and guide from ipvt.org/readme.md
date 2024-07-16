## 2.2 Customized m3u playlist and scheduled guide generation from iptv.org
If you use m3u streams from [iptv.org](https://github.com/iptv-org/iptv) and wants your own custom m3u playlist as well as generate it's guide.xml using [epg](https://github.com/iptv-org/epg) on a schedule, then this is the script for you. I wrote this to use in a windows machine hence powershell. You may use gpt to convert this to your language of choice.

1. Get all the files "2.2. Customized TV playlist and guide from ipvt.org".

<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/44327790-2469-4b6a-aa77-0cd0012eaadd" alt="Creation Example" width="500" height="auto">

1. Add Tv channels you want in tv.json.

<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/2f53f117-9320-4340-90ec-af83865ef460" alt="Creation Example" width="auto" height="500">

1. You may manualy run the 'updateTV.ps1' manually or schedule it.
2. You can automate the running of 'updateTV.ps1' by running 'updateTV_Scheduler.ps1' a service. Change the path pointing to 'updateTV.ps1' as well as the schedule as needed.

<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/ab01ffb9-cc1c-4af3-bd56-44360cc246aa" alt="Creation Example" width="auto" height="auto">

6. Setup 'updateTV_Scheduler.ps1' as a service using [NSSM](https://nssm.cc/).
After downloading NSSM, using cmd, cd to the nssm folder and run this command after updating the path to your scheduler script 'updateTV_Scheduler.ps1':
```
nssm install updateTv "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" "-NoProfile -WindowStyle Hidden -File C:\path_to\updateTV_Scheduler.ps1"
```
Use this command to edit the service using nssm if needed.
```
nsssm edit updateTv
```
