# Narration Studio launcher
# Based on run_gradio.ps1

# Find where the latest MSVC is installed dynamically
$vswherePath = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"

if (Test-Path $vswherePath) {
    $vcvarsPath = & $vswherePath -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
    if ($vcvarsPath) {
        $vcvarsPath = Join-Path $vcvarsPath "VC\Auxiliary\Build\vcvars64.bat"
    }
} else {
    Write-Host "ERROR: vswhere.exe not found! Please ensure Visual Studio is installed." -ForegroundColor Red
}

# Ensure the path is valid
if (Test-Path $vcvarsPath) {
    Write-Host "Setting up MSVC environment..." -ForegroundColor Yellow
    & cmd /c "`"$vcvarsPath`" && set" | ForEach-Object {
        if ($_ -match "^(.*?)=(.*)$") {
            Set-Item -Path "env:$($matches[1])" -Value "$($matches[2])"
        }
    }
} else {
    Write-Host "ERROR: vcvars64.bat could not be found! Please make sure MSVC is installed properly." -ForegroundColor Red
    Write-Host "Continuing without MSVC..." -ForegroundColor Yellow
}

# Activate python venv
Set-Location $PSScriptRoot

if ($env:OS -ilike "*windows*") {
  if (Test-Path "./venv/Scripts/Activate.ps1") {
    Write-Output "Windows venv"
    . ./venv/Scripts/Activate.ps1
  }
  elseif (Test-Path "./.venv/Scripts/Activate.ps1") {
    Write-Output "Windows .venv"
    . ./.venv/Scripts/Activate.ps1
  }
}
elseif (Test-Path "./venv/bin/Activate.ps1") {
  Write-Output "Linux venv"
  . ./venv/bin/Activate.ps1
}
elseif (Test-Path "./.venv/bin/activate") {
  Write-Output "Linux .venv"
  . ./.venv/bin/activate
}

$Env:HF_HOME = $PSScriptRoot + "\huggingface"
$Env:TORCH_HOME = $PSScriptRoot + "\torch"
$Env:XFORMERS_FORCE_DISABLE_TRITON = "1"
$Env:CUDA_HOME = "${env:CUDA_PATH}"
$Env:PHONEMIZER_ESPEAK_LIBRARY = "C:\Program Files\eSpeak NG\libespeak-ng.dll"
$Env:GRADIO_HOST = "127.0.0.1"

Write-Host "Starting Narration Studio..." -ForegroundColor Green
Write-Host "Batch TTS with multi-voice support" -ForegroundColor Cyan

python narration_studio.py

Read-Host "Press Enter to exit" | Out-Null
