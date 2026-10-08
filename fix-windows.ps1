# Antigravity 403 / 503 & Session Reset Helper for Windows
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   Antigravity Fixer for Windows PowerShell       " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Kill processes
Write-Host "`n[*] Terminating any hanging Antigravity processes..." -ForegroundColor Yellow
Stop-Process -Name *antigravity* -Force -EA 0
Write-Host "[✓] Background processes stopped." -ForegroundColor Green

# 2. Reset local cache
Write-Host "`n[*] Cleaning session cache in ~/.antigravity & ~/.gemini..." -ForegroundColor Yellow
Remove-Item -Recurse -Force "$HOME\.antigravity" -EA 0
Remove-Item -Recurse -Force "$HOME\.gemini" -EA 0
Write-Host "[✓] Cache directories wiped." -ForegroundColor Green

# 3. Check for validation_url in logs
$logPaths = @(
    "$env:LOCALAPPDATA\hermes\logs\errors.log",
    "$HOME\.hermes\logs\errors.log",
    "$env:APPDATA\Antigravity\logs\language_server.log",
    "$env:APPDATA\Antigravity\logs\main.log"
)

$foundUrl = $null

foreach ($log in $logPaths) {
    if (Test-Path $log) {
        $content = Get-Content $log -Tail 200 -EA 0
        foreach ($line in $content) {
            if ($line -match '(https://accounts\.google\.com/signin/continue\?[^\s"''\\]+)') {
                $foundUrl = $matches[1]
            }
        }
        if ($foundUrl) { break }
    }
}

if ($foundUrl) {
    Write-Host "`n[!] Found Google Human Verification URL:" -ForegroundColor Yellow
    Write-Host $foundUrl -ForegroundColor Cyan
    Write-Host "`n[*] Launching in browser..." -ForegroundColor Yellow
    Start-Process $foundUrl
    Write-Host "[✓] Complete verification in browser, then retry Antigravity." -ForegroundColor Green
} else {
    Write-Host "`n[✓] No pending validation URLs detected. Session cleaned successfully." -ForegroundColor Green
}
