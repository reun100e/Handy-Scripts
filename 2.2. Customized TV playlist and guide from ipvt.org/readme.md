# Custom TV Playlist & EPG Generator (Local Repo Edition)

This PowerShell script generates a custom Jellyfin-compatible M3U playlist and XMLTV EPG guide by:
1.  Reading channels from a local `iptv-org/iptv` repository.
2.  Fetching accurate EPG data from a local `iptv-org/epg` repository (specifically `tataplay.com` and `dishtv.in`).
3.  Validating that streams are online before adding them.
4.  Allowing custom (paid/private) stream URLs.

## Prerequisites

1.  **PowerShell 5.1** or later (Standard on Windows).
2.  **Node.js** (Required for EPG generation). [Download Here](https://nodejs.org/).
3.  **Git** (Required for updating repositories). [Download Here](https://git-scm.com/).

## Setup Instructions

### 1. Folder Structure
Ensure your folder looks like this:
```text
/MyScriptFolder
    |--- updateTV.ps1
    |--- tv.json
    |--- Fix-LanguageMode.ps1 (Optional help script)
    |--- iptv/               <-- Cloned Repo
    |--- epg/                <-- Cloned Repo
```

### 2. Initial Setup
The script will **automatically** clone the required repositories (`iptv` and `epg`) if they are missing.
However, you need to ensure `git` and `npm` are installed.

1.  Copy `updateTV.ps1` and `tv.json` to your server folder.
2.  Run the script once to let it setup the folders:
    ```powershell
    .\updateTV.ps1
    ```

### 3. Channel Selection
The script supports two modes of operation:

**A. Strict Mode (Recommended)**
Only includes channels explicitly listed in `tv.json`.
Enable it in `tv.json`:
```json
"_settings": {
  "strict_mode": true
}
```

**B. Standard Mode**
Loads ALL channels from the base playlist (India) and allows you to `exclude` specific ones.
(Default behavior if `strict_mode` is missing or false).

### 4. Logging
A log file `update.log` is generated in the script directory. It tracks:
*   Timestamp of every run.
*   Playlist generation stats (count of channels).
*   EPG Grabber summary (channels found, success status).

### 5. Running the Script
Run the PowerShell script:
```powershell
.\updateTV.ps1
```

**Options:**
*   `-SkipValidation`: Skips the "Is Stream Online?" check. Useful if you are offline or identifying channels without waiting for network timeouts.
    ```powershell
    .\updateTV.ps1 -SkipValidation
    ```

### Automation (Daily Task)
To run this automatically every day (e.g., at 4 AM) so your TV guide is always fresh:

1.  Open PowerShell as Administrator.
2.  Run the following command (adjust path if needed):

```powershell
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$PSScriptRoot\updateTV.ps1`""
$Trigger = New-ScheduledTaskTrigger -Daily -At 4am
Register-ScheduledTask -TaskName "UpdateTVPlaylist" -Action $Action -Trigger $Trigger -Description "Updates IPTV Playlist and Guide daily"
```

## How It Works in Detail
1.  **Auto-Update**: The script runs `git pull` on `iptv` and `epg` folders to get the latest data.
2.  **Playlist Generation**: It scans `iptv/streams/in.m3u` (India) for your requested channels.
3.  **Custom Streams**: If you provided a `url` in `tv.json`, it uses that priority.
4.  **EPG Matching**: It looks up the channel name in `epg/sites/tataplay.com.channels.xml` (and `dishtv.in`). If found, it assigns the correct `xmltv_id`.
5.  **Generation**:
    *   Creates `filtered_playlist.m3u` (The Playlist).
    *   Runs the Node.js EPG grabber to create `guideXMLTV.xml` (The Guide).

## Troubleshooting

**"Security Warning" or "Constrained Language Mode"**
*   The script includes fixes for restricted environments.
*   If you still see errors, try running `Fix-LanguageMode.ps1` as Administrator and rebooting.

**"No Valid Stream"**
*   The script validates streams by trying to connect to them. If a public stream is down (common with free IPTV), it is skipped.
*   Use `-SkipValidation` to include them anyway if you want to verify the EPG.
