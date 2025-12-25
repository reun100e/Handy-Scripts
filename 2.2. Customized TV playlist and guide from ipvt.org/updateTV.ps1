# PowerShell Script to Update TV Playlist and Guide using Local Repositories
# Version: 3.1 (Local Repo Edition + Offline Mode)

param (
    [switch]$SkipValidation = $false
)

# Configuration Paths
$ScriptDir = $PSScriptRoot
$TvJsonPath = Join-Path $ScriptDir "tv.json"
$PlaylistPath = Join-Path $ScriptDir "filtered_playlist.m3u"
$EpgConfigPath = Join-Path $ScriptDir "filtered_channels.xml"
$GuidePath = Join-Path $ScriptDir "guideXMLTV.xml"
$IptvRepoPath = Join-Path $ScriptDir "iptv"
$EpgRepoPath = Join-Path $ScriptDir "epg"
$LogFile = Join-Path $ScriptDir "update.log"

function Write-Log {
    param ([string]$Message)
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$TimeStamp] $Message"
    Add-Content -Path $LogFile -Value $LogEntry
    # Optional: Write to host as well if not already doing so
}

Write-Log "========================================"
Write-Log "Starting TV Update Script v3.1"
Write-Log "========================================"

# Ensure Local Repos Exist (Auto-Clone)
if (-not (Test-Path $IptvRepoPath)) {
    Write-Host "Cloning 'iptv' repository..." -ForegroundColor Yellow
    git clone https://github.com/iptv-org/iptv.git $IptvRepoPath
}
if (-not (Test-Path $EpgRepoPath)) {
    Write-Host "Cloning 'epg' repository..." -ForegroundColor Yellow
    git clone https://github.com/iptv-org/epg.git $EpgRepoPath
    
    # Auto-install dependencies for EPG
    if (Test-Path $EpgRepoPath) {
        Push-Location $EpgRepoPath
        Write-Host "Installing EPG dependencies..." -ForegroundColor Yellow
        npm install
        Pop-Location
    }
}

# Update Local Repositories to get latest channels/fixes
if (-not $SkipValidation) {
    Write-Host "Updating Local Repositories..." -ForegroundColor Yellow
    foreach ($repo in @($IptvRepoPath, $EpgRepoPath)) {
        Push-Location $repo
        if (Test-Path ".git") {
            try {
                git pull --quiet
                Write-Host "Updated $(Split-Path $repo -Leaf)" -ForegroundColor Cyan
            } catch {
                Write-Warning "Failed to update $(Split-Path $repo -Leaf)"
            }
        }
        Pop-Location
    }
}

# Update Local Repositories to get latest channels/fixes
if (-not $SkipValidation) {
    Write-Host "Updating Local Repositories..." -ForegroundColor Yellow
    foreach ($repo in @($IptvRepoPath, $EpgRepoPath)) {
        Push-Location $repo
        if (Test-Path ".git") {
            try {
                git pull --quiet
                Write-Host "Updated $(Split-Path $repo -Leaf)" -ForegroundColor Cyan
            } catch {
                Write-Warning "Failed to update $(Split-Path $repo -Leaf)"
            }
        }
        Pop-Location
    }
}

# --- FUNCTIONS ---

function Parse-M3UFile {
    param ([string]$FilePath)
    Write-Host "Parsing M3U: $FilePath" -ForegroundColor Cyan
    
    $channels = @()
    if (Test-Path $FilePath) {
        $lines = Get-Content $FilePath
        $currentChannel = @{}

        foreach ($line in $lines) {
            $line = $line.Trim()
            if ($line.StartsWith("#EXTINF")) {
                $currentChannel = @{}
                # Extract basic metadata
                if ($line -match 'tvg-id="([^"]*)"') { $currentChannel["TvgId"] = $matches[1] }
                if ($line -match 'tvg-logo="([^"]*)"') { $currentChannel["Logo"] = $matches[1] }
                if ($line -match 'group-title="([^"]*)"') { $currentChannel["Group"] = $matches[1] }
                
                # Extract Name (everything after the last comma)
                $nameStyles = $line -split ","
                $currentChannel["Name"] = $nameStyles[-1].Trim()
                $currentChannel["RawInfo"] = $line
            }
            elseif ($line -match "^https?") {
                if ($currentChannel.Keys.Count -gt 0) {
                    $currentChannel["Url"] = $line
                    # Use Hashtable directly
                    $channels += $currentChannel
                    $currentChannel = @{} # Reset
                }
            }
        }
    } else {
        Write-Warning "File not found: $FilePath"
    }
    return $channels
}

function Load-EpgSiteIds {
    # Loads TataPlay and DishTV mappings for better EPG
    $sites = @("tataplay.com", "dishtv.in")
    $mappings = @{} # Key: ChannelName (normalized), Value: {Site, SiteId, XmlTvId}

    foreach ($site in $sites) {
        $xmlPath = Join-Path $EpgRepoPath "sites\$site\$site.channels.xml"
        if (Test-Path $xmlPath) {
            Write-Host "Loading EPG IDs from $site..." -ForegroundColor Cyan
            try {
                # Load XML using standard cast (Property access is safe)
                [xml]$xml = Get-Content $xmlPath
                foreach ($node in $xml.channels.channel) {
                    # Avoid methods like Trim() if possible, but string methods are usually core.
                    # Use property access for attributes (PowerShell wraps XML attributes as properties)
                    $nameText = "$($node.'#text')"
                    $nameNorm = $nameText.ToLower().Trim()
                    
                    if (-not $mappings[$nameNorm]) {
                        $mappings[$nameNorm] = @{
                            Site = "$($node.site)"
                            SiteId = "$($node.site_id)"
                            XmlTvId = "$($node.xmltv_id)"
                            Name = $nameText
                        }
                    }
                }
            } catch {
                Write-Warning "Failed to load XML for $site : $_"
            }
        }
    }
    return $mappings
}

function Test-StreamValidity {
    param (
        [string]$Url,
        [int]$TimeoutSec = 4
    )
    
    # In Constrained Language Mode, .NET types like HttpWebRequest might be blocked.
    # Use Invoke-WebRequest which is a native Cmdlet.
    try {
        # Use HEAD method first
        $response = Invoke-WebRequest -Uri $Url -Method Head -TimeoutSec $TimeoutSec -ErrorAction Stop -UserAgent "VLC/3.0.18 LibVLC/3.0.18" -UseBasicParsing
        if ($response.StatusCode -eq 200) { return $true }
    }
    catch {
        # Fallback to GET with range if HEAD not supported/fails
        try {
             # Note: Invoke-WebRequest doesn't support Range header natively in older PS5 easily without custom headers
             # But let's try a standard GET
             $response = Invoke-WebRequest -Uri $Url -Method Get -TimeoutSec $TimeoutSec -ErrorAction Stop -UserAgent "VLC/3.0.18 LibVLC/3.0.18" -UseBasicParsing
             if ($response.StatusCode -eq 200) { return $true }
        } catch {
             return $false
        }
    }
    return $false
}

# --- MAIN LOGIC ---

# 1. Load User Requests/Config
Write-Host "Reading tv.json..." -ForegroundColor Yellow
$jsonContent = Get-Content $TvJsonPath -Raw
$userConfig = $jsonContent | ConvertFrom-Json

# Check Strict Mode
$settings = $userConfig | Where-Object { $_._settings } | Select-Object -ExpandProperty _settings -ErrorAction SilentlyContinue
$strictMode = $false
if ($settings.strict_mode) { $strictMode = $true }

# 2. Load Base Playlist (Pre-load India for reference or base)
$baseM3u = Join-Path $IptvRepoPath "streams\in.m3u"
$baseChannels = @()
if (Test-Path $baseM3u) { $baseChannels = Parse-M3UFile -FilePath $baseM3u }

$masterList = @()
if (-not $strictMode) {
    Write-Host "Loading Base Playlist (India)..." -ForegroundColor Yellow
    $masterList = $baseChannels
    Write-Host "Base Channels Loaded: $($masterList.Count)" -ForegroundColor Green
} else {
    Write-Host "Strict Mode: Starting with empty playlist." -ForegroundColor Magenta
}

# 3. Load EPG Mappings
$epgMap = Load-EpgSiteIds

# 4. Helper: Global Search Function
function Find-ChannelGlobally {
    param ($Name, $Id)
    $allM3us = Get-ChildItem -Path (Join-Path $IptvRepoPath "streams") -Filter "*.m3u" | Where-Object { $_.Name -ne "in.m3u" }
    foreach ($file in $allM3us) {
        if (Select-String -Path $file.FullName -Pattern $Name -SimpleMatch -Quiet) {
            $fileChannels = Parse-M3UFile -FilePath $file.FullName
            
            # Exact Match
            $found = $fileChannels | Where-Object { $_.Name -eq $Name -or ($Id -and $_.TvgId -eq $Id) } | Select-Object -First 1
            
            # Fuzzy Match fallback
            if (-not $found) {
                $found = $fileChannels | Where-Object { $_.Name -like "*$Name*" } | Select-Object -First 1
            }
            
            if ($found) { 
                $found.RawInfo = $file.Name # Store source info
                return $found 
            }
        }
    }
    return $null
}

# 5. Process Configuration
Write-Host "`nProcessing Configuration..." -ForegroundColor Yellow

$finalPlaylist = @()

if (-not $strictMode) {
    # Blocklist Logic
    $excludedNames = ($userConfig | Where-Object { $_.exclude -eq $true }).name
    if ($excludedNames) {
        Write-Host "Excluding $($excludedNames.Count) channels..." -ForegroundColor Magenta
        $masterList = $masterList | Where-Object { $excludedNames -notcontains $_.Name }
    }
    $finalPlaylist = $masterList
}

# Additions / Strict Processing
$itemsToProcess = $userConfig | Where-Object { -not $_.exclude -and -not $_._settings -and -not $_._comment }

foreach ($req in $itemsToProcess) {
    if (-not $req.name) { continue }
    $reqName = $req.name
    $reqId = $req.'tvg-id'
    $reqUrl = $req.url

    # Non-Strict: Skip if already present
    if (-not $strictMode -and ($finalPlaylist | Where-Object { $_.Name -eq $reqName })) { continue }

    Write-Host "Processing: $reqName" -NoNewline
    $newStream = $null

    # 1. Custom
    if ($reqUrl) {
         Write-Host " [Custom URL]" -ForegroundColor Magenta
         $newStream = @{ Name = $reqName; TvgId = $reqId; Url = $reqUrl; Source = "Custom" }
    } 
    # 2. Check India Base (Fast)
    elseif ($baseChannels) {
        # Try Exact first
        $found = $baseChannels | Where-Object { $_.Name -eq $reqName } | Select-Object -First 1
        
        # Try Fuzzy (Substring) if Strict Mode
        if (-not $found -and $strictMode) {
            $found = $baseChannels | Where-Object { $_.Name -like "*$reqName*" } | Select-Object -First 1
            if ($found) { Write-Host " [Fuzzy Match: $($found.Name)]" -NoNewline -ForegroundColor Gray }
        }

        if ($found) {
            Write-Host " [Found in India]" -ForegroundColor Green
            $newStream = $found
        }
    }
    
    # 3. Global Search
    if (-not $newStream) {
        Write-Host " [Searching Global...]" -NoNewline
        $foundGlobal = Find-ChannelGlobally -Name $reqName -Id $reqId
        if ($foundGlobal) {
            Write-Host " Found in $($foundGlobal.RawInfo)" -ForegroundColor Cyan
            $newStream = $foundGlobal
        } else {
            Write-Host " Not Found" -ForegroundColor Red
        }
    }

    # Validate and Add
    if ($newStream) {
        if ($SkipValidation) {
             # Trust it
        } elseif (-not (Test-StreamValidity -Url $newStream.Url)) {
            Write-Host " [Stream Offline]" -ForegroundColor Red
            continue 
        }
        
        $finalPlaylist += $newStream
    }
}


# 6. EPG Matching & Final Validation Loop
# Now we iterate the ENTIRE final playlist (Base + Added) to attach EPG
Write-Host "`nFinalizing Playlist & EPG ($($finalPlaylist.Count) channels)..." -ForegroundColor Yellow

$processedPlaylist = @()
$epgConfigList = @()

foreach ($stream in $finalPlaylist) {
    # Optional: Skip validation for *base* channels to speed up? 
    # User wanted "Show All", but 600 validation checks takes time.
    # Decision: Validating 600 streams takes ~30 mins. 
    # We should probably ONLY validate if user didn't say -SkipValidation.
    
    if (-not $SkipValidation) {
        if (-not (Test-StreamValidity -Url $stream.Url)) {
            # Skip offline channels from the base list too
            continue
        }
    }

    # EPG Lookup
    $epgData = $null
    
    # Priority 1: Lookup by Stream Name
    if ($stream.Name) { $epgData = $epgMap[$stream.Name.ToLower()] }
    
    # Priority 2: Lookup by TvgId if it looks like a name (fallback)
    if (-not $epgData -and $stream.TvgId) { $epgData = $epgMap[$stream.TvgId.Split(".")[0].ToLower()] }

    if ($epgData) {
        $stream.TvgId = $epgData.XmlTvId
        # Add to EPG Config
        $epgConfigList += @{
            Site = $epgData.Site
            SiteId = $epgData.SiteId
            XmlTvId = $epgData.XmlTvId
            Name = $stream.Name
        }
    }
    
    $processedPlaylist += $stream
}

# 5. Write Playlist
Write-Host "`nWriting Playlist to $PlaylistPath..." -ForegroundColor Yellow
$m3uContent = "#EXTM3U`n"
foreach ($chan in $processedPlaylist) {
    # Construct EXTINF line
    $logo = if ($chan.Logo) { " tvg-logo=`"$($chan.Logo)`"" } else { "" }
    $id = if ($chan.TvgId) { " tvg-id=`"$($chan.TvgId)`"" } else { "" }
    $group = if ($chan.Group) { " group-title=`"$($chan.Group)`"" } else { "" }
    
    $m3uContent += "#EXTINF:-1$id$logo$group,$($chan.Name)`n"
    $m3uContent += "$($chan.Url)`n"
}
Set-Content -Path $PlaylistPath -Value $m3uContent -Encoding UTF8
Set-Content -Path $PlaylistPath -Value $m3uContent -Encoding UTF8
Set-Content -Path $PlaylistPath -Value $m3uContent -Encoding UTF8
Write-Host "Playlist Saved. ($($finalPlaylist.Count) channels)" -ForegroundColor Green
Write-Log "Playlist generated. Total Channels: $($finalPlaylist.Count)"
Write-Log "Playlist saved to $PlaylistPath"

# 6. Generate EPG (using local epg repo scripts)
if ($epgConfigList.Count -gt 0) {
    Write-Host "`nGenerating EPG Config..." -ForegroundColor Yellow
    
    # Create the channels.xml format expected by iptv-org/epg
    $xmlContent = "<?xml version=`"1.0`" encoding=`"UTF-8`"?>`n<channels>`n"
    foreach ($item in $epgConfigList) {
        $xmlContent += "  <channel site=`"$($item.Site)`" site_id=`"$($item.SiteId)`" xmltv_id=`"$($item.XmlTvId)`">$($item.Name)</channel>`n"
    }
    $xmlContent += "</channels>"
    
    Set-Content -Path $EpgConfigPath -Value $xmlContent -Encoding UTF8

    Write-Host "Running EPG Grabber..." -ForegroundColor Yellow
    # Navigate to EPG repo and run grab
    Push-Location $EpgRepoPath
    
    # Ensure dependencies are installed (first run only, effectively)
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installing EPG dependencies..."
        npm install
    }

    # Run the grabber
    # Note: 'npm run grab' syntax might vary. The standard is check package.json.
    # Usually: npx tcp-grab --channels=... --output=...
    # Or via the script defined in package.json
    
    try {
       # Use npx tsx directly to avoid npm argument parsing issues
       $grabScript = Join-Path $EpgRepoPath "scripts\commands\epg\grab.ts"
       # Ensure we use the local npx/tsx from the repo if possible, or global. 
       # Simpler: just use the npm run command but format it carefully.
       # Actually, npx tsx is safer if installed.
       
       Write-Host "Executing EPG grabber..." -ForegroundColor Cyan
       Write-Log "Starting EPG Grabber..."
       
       $grabCmd = "npx tsx `"$grabScript`" --channels=`"$EpgConfigPath`" --output=`"$GuidePath`" --maxConnections=5"
       
       # Capture output to variable, redirect stderr to stdout
       $epgOutput = cmd /c $grabCmd 2>&1
       
       # Show to user
       $epgOutput | Write-Host
       
       # Log only summary lines (reduce size)
       $epgOutput | ForEach-Object { 
            # Remove potential null bytes or excessive spacing for matching
            $clean = $_ -replace "\0", "" -replace "\s+", ""
            
            if ($clean -match "success" -or 
                $clean -match "error" -or 
                $clean -match "found\d+channel") {
                
                # Write a clean version to the log (single spaced)
                # Collapse multiple spaces to one, remove nulls
                $logLine = ($_ -replace "\0", "") -replace "\s+", " "
                Write-Log "EPG: $logLine" 
            }
       }
       
       if ($LASTEXITCODE -eq 0) {
           Write-Host "EPG Generation Complete!" -ForegroundColor Green
           Write-Log "EPG Generation Complete."
       } else {
           Write-Error "EPG Grabbing failed with exit code $LASTEXITCODE"
           Write-Log "ERROR: EPG Grabbing failed with exit code $LASTEXITCODE"
       }
    } catch {
       Write-Error "EPG Generation Failed: $_"
    }
    
    Pop-Location
} else {
    Write-Host "No EPG targets found to grab." -ForegroundColor Yellow
}

Write-Host "`nUpdate Complete!" -ForegroundColor Green