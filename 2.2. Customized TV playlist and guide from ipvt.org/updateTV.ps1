# CHECK FOR ACTIVE INTERNET AND WAIT FOR ONE IF NEEDED

function Wait-ForInternetConnection {
    param (
        [int]$DelayInSeconds = 10
    )

    while ($true) {
        try {
            $request = [System.Net.WebRequest]::Create("http://www.google.com")
            $request.Timeout = 5000
            $response = $request.GetResponse()
            if ($response.StatusCode -eq 200) {
                break
            }
        }
        catch {
            Write-Host "No internet connection. Waiting for $DelayInSeconds seconds before retrying..."
            Start-Sleep -Seconds $DelayInSeconds
        }
    }
}

#UPDATING PLAYLIST

$tvJsonPath = ".\tv.json"
$m3uUrl = "https://iptv-org.github.io/iptv/index.m3u"
$newM3uFilePath = ".\filtered_playlist.m3u"
$availableChannelsJsonFilePath = ".\available_channels.json"

# Wait for internet connecion
Wait-ForInternetConnection
# Download the M3U file from the internet
Write-Host "Updating Tv channels from iptv.org."
$m3uContent = Invoke-RestMethod -Uri $m3uUrl -Method Get -UseBasicParsing

# Load the JSON file
$channelsToCheck = Get-Content -Path $tvJsonPath | ConvertFrom-Json

function ParseM3U {
    param ([string]$m3uContent)

    $channels = @()
    $lines = $m3uContent -split "`n"
    for ($i = 0; $i -lt $lines.Length; $i++) {
        if ($lines[$i] -match "^#EXTINF") {
            $channelInfo = $lines[$i]
            $channelUrl = $lines[$i + 1]
            $channels += [PSCustomObject]@{
                Info = $channelInfo
                Url  = $channelUrl
            }
            $i++
        }
    }
    return $channels
}

$m3uChannels = ParseM3U $m3uContent
$matchedChannels = @()

Write-Host "Collecting subscribed channels (see tv.json)."
foreach ($channel in $channelsToCheck) {
    $matchedChannel = $m3uChannels | Where-Object { $_.Info -match $channel.name }
    if ($matchedChannel) {
        $matchedChannels += $matchedChannel
    }
}

"#EXTM3U" | Out-File -FilePath $newM3uFilePath -Encoding UTF8

foreach ($channel in $matchedChannels) {
    $channel.Info | Out-File -FilePath $newM3uFilePath -Append -Encoding UTF8
    $channel.Url | Out-File -FilePath $newM3uFilePath -Append -Encoding UTF8
}

$uniqueChannels = $m3uChannels | Sort-Object -Property Url -Unique
$availableChannelsJson = $uniqueChannels | ForEach-Object {
    $channelName = if ($_ -match 'tvg-id="([^"]+)"') { $matches[1] } else { $_.Info }
    [PSCustomObject]@{
        name = $channelName
        url  = $_.Url
    }
} | ConvertTo-Json -Depth 2

$availableChannelsJson | Out-File -FilePath $availableChannelsJsonFilePath -Encoding UTF8

Write-Output "Filtered playlist created: $newM3uFilePath"
Write-Output "Available channels JSON created: $availableChannelsJsonFilePath"

#UPDATING CHANNELS

# Define paths
$repoPath = ".\epg"
$outputXmlPath = ".\filtered_channels.xml"

# Change directory to the repository path
Set-Location -Path $repoPath

# Wait for internet connecion
Wait-ForInternetConnection

# Pull the latest changes from the GitHub repository
Write-Host "Updating subscribed channel data from iptv.org."
git pull

# Change back to the original directory to access tv.json and save filtered_channels.xml
Set-Location ..

# Load tv.json
$tvJson = Get-Content -Path $tvJsonPath | ConvertFrom-Json

Write-Host "Filtering channels."
# Initialize filtered_channels.xml
$xmlContent = @()
$xmlContent += '<?xml version="1.0" encoding="UTF-8"?>'
$xmlContent += '<channels>'

# Search for corresponding lines in all .xml files within nested folders
$xmlFiles = Get-ChildItem -Path "$repoPath\sites" -Recurse -Filter *.xml

foreach ($tvEntry in $tvJson) {
    $channelName = $tvEntry.name

    foreach ($xmlFile in $xmlFiles) {
        $lines = Get-Content -Path $xmlFile.FullName
        foreach ($line in $lines) {
            if ($line -like "*$channelName*") {
                $xmlContent += $line
            }
        }
    }
}

$xmlContent += '</channels>'

# Write to filtered_channels.xml
$xmlContent | Out-File -FilePath $outputXmlPath -Encoding utf8
Write-Host "Filtering channels completed successfully."
Write-Host "Filtered channels XML has been created at $outputXmlPath"

#GENERATING GUIDE

Write-Host "Generating channel guides."

# Define the path to the custom channels XML file
$customChannelsPath = "../filtered_channels.xml"

# Define the directory of the repository
$repoDirectory = ".\epg"

# Change to the repository directory
Set-Location -Path $repoDirectory

Write-Host "Installing IPTV epg."
# Ensure npm dependencies are installed (optional, depending on your setup)
npm install

# Wait for internet connecion
Wait-ForInternetConnection

Write-Host "Grabbing channels guides."
# Run the grab command with the custom channels file
npm run grab -- --channels=$customChannelsPath

# Output a success message
Write-Output "EPG generation completed successfully."

Set-Location ..

# MAKE guide.xml USABLE FOR JELLYFIN

# Define input and output file paths
$inputFile = "C:\update TV\epg\guide.xml"
$outputFile = "C:\update TV\guideXMLTV.xml"

# Read the content of the input file
$content = Get-Content -Path $inputFile -Raw

# Replace the encoding in the first line from "UTF-8" to "ISO-8859-1"
$content = $content -replace 'encoding="UTF-8"', 'encoding="ISO-8859-1"'

# Replace unescaped ampersands with &amp;
# This regex ensures that it does not replace already escaped & (i.e., &amp;, &lt;, &gt;, etc.)
$escapedContent = $content -replace '(&)(?!amp;|lt;|gt;|quot;|apos;)', '&amp;'

# Write the escaped content to the output file
Set-Content -Path $outputFile -Value $escapedContent

Write-Host "Encoding has been changed and ampersands in $inputFile have been escaped. The result has been saved to $outputFile"

Write-Output "TV Guide updated successfully."

Start-Sleep -Seconds 10
