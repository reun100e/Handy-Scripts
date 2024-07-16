# updateTV_Scheduler.ps1
$taskName = "updateTV"
$scriptPath = "C:\update TV\updateTV.ps1"

# Remove existing task if it exists
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Define the trigger
$trigger = New-ScheduledTaskTrigger -Daily -At "5:00AM"

# Define the action
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -File $scriptPath"

# Register the task
Register-ScheduledTask -TaskName $taskName -Trigger $trigger -Action $action -RunLevel Highest -User "SYSTEM"
