Set-Location $PSScriptRoot

# Set eSpeak library path
$Env:PHONEMIZER_ESPEAK_LIBRARY = "C:\Program Files\eSpeak NG\libespeak-ng.dll"

Write-Host "Testing Zonos with RTX 5090..." -ForegroundColor Green

# Run the test
.\.venv\Scripts\python.exe sample_rtx5090.py

Write-Host "`nTest complete!" -ForegroundColor Green
Read-Host "Press Enter to exit"
