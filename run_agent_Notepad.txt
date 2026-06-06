# Run Gmail Calendar AI Agent
# This script runs the Gmail-to-Calendar agent using uv

Set-Location "C:\michal-sharon-privet-api"

$logFile = "C:\michal-sharon-privet-api\agent_run.log"

Add-Content $logFile "----------------------------------------"
Add-Content $logFile "Agent started at: $(Get-Date)"

try {
    uv run python gmail_calendar_agent.py *>> $logFile
    Add-Content $logFile "Agent finished successfully at: $(Get-Date)"
}
catch {
    Add-Content $logFile "ERROR at: $(Get-Date)"
    Add-Content $logFile $_.Exception.Message
}