# 1. Clear files older than 30 days to free space
Get-ChildItem 'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\logs_v2\*' -Recurse | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item -Force

# 2. Restart the Watchdog Service to ensure memory refresh
Stop-ScheduledTask -TaskName 'MuZero_Watchdog_Service'
Start-Sleep -Seconds 5
Start-ScheduledTask -TaskName 'MuZero_Watchdog_Service'

Write-Host "Daily maintenance completed: 06/18/2026 02:37:10"
