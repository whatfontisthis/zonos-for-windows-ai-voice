Set-Location $PSScriptRoot

# Disable CUDA to force CPU usage
$env:CUDA_VISIBLE_DEVICES = ""

# Run the CPU test
.\.venv\Scripts\python.exe sample_cpu.py

Read-Host "Press Enter to exit"
