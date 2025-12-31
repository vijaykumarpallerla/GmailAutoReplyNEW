# PowerShell script to run gmail_pull management command
# Adjust interval via Task Scheduler (recommended: 1-5 minutes; avoid <30s for Gmail API quota)

$ErrorActionPreference = 'SilentlyContinue'
$projectDir = "C:\Users\Palle\OneDrive\Desktop\Gmail Auto Reply"
$venvPython = Join-Path $projectDir 'venv\Scripts\python.exe'
$managePy = Join-Path $projectDir 'manage.py'
$logFile = Join-Path $projectDir 'gmail_pull.log'

# Ensure OAUTHLIB_INSECURE_TRANSPORT for local HTTP dev
$env:OAUTHLIB_INSECURE_TRANSPORT = 1

# Run pull (empty query means default service behavior)
& $venvPython $managePy gmail_pull >> $logFile 2>&1

# OPTIONAL: rotate log if >2MB
if ((Test-Path $logFile) -and ((Get-Item $logFile).Length -gt 2MB)) {
    $archive = Join-Path $projectDir ("gmail_pull_" + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
    Move-Item $logFile $archive -Force
}
