# 2.1 Cast photos not appearing in Jellyfin
In Jellyfin, sometimes the cast photo doesn't show unless the cast page is visited once. This script visits all the cast pages in you Jellyfin so that you don't have to spend another month clicking every cast image. Setup an API from Jellyfin admin settings, give it to the script, and point it to server url - the script will do its job. The script is not mine. It's from [here](https://github.com/jellyfin/jellyfin/issues/8103). This is temporary fix and the issue will likely be fixed in future versions.

<img src="https://github.com/reun100e/Handy-Scripts/assets/47780896/c03627b2-30fb-40c4-9e90-edfbf5ca9797" alt="Creation Example" width="auto" height="auto">

```
python Jellyfin-repair-cast-not-showing.py
```
