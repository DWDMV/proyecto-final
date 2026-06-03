param(
    [string]$OutputDir = $null
)

# Exit script on first error
$ErrorActionPreference = "Stop"

# Get directory where the script is located
$ScriptDir = $PSScriptRoot

# Resolve project root (two levels up from src/scripts)
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $ScriptDir "..\.."))

# Configuration
$UrlFile = Join-Path $ProjectRoot "data\url.txt"

if ([string]::IsNullOrEmpty($OutputDir)) {
    $OutputDir = Join-Path $ProjectRoot "data"
}

# Check if URL file exists
if (-not (Test-Path $UrlFile)) {
    Write-Error "Error: URL file not found at $UrlFile"
    exit 1
}

# Read and trim the URL
$Url = (Get-Content $UrlFile -Raw).Trim()

if ([string]::IsNullOrWhiteSpace($Url)) {
    Write-Error "Error: URL file is empty or contains only whitespace."
    exit 1
}

# Ensure output directory exists
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
}

# Define temporary zip file path
$ZipPath = Join-Path $OutputDir "temp_data.zip"

Write-Host "Reading URL from: $UrlFile"
Write-Host "Target URL: $Url"
Write-Host "Downloading to: $ZipPath"

try {
    # Download file using Invoke-WebRequest
    # -UseBasicParsing is used to avoid dependency on Internet Explorer engine
    Invoke-WebRequest -Uri $Url -OutFile $ZipPath -UseBasicParsing
}
catch {
    Write-Error "Error: Failed to download the file from $Url. Details: $_"
    exit 1
}

Write-Host "Download complete. Unzipping to: $OutputDir"

try {
    # Unzip file
    # -Force to overwrite existing files without prompting
    Expand-Archive -Path $ZipPath -DestinationPath $OutputDir -Force
}
catch {
    Write-Error "Error: Failed to unzip $ZipPath. Details: $_"
    # Clean up the zip file even on failure to avoid leaving junk
    if (Test-Path $ZipPath) {
        Remove-Item -Path $ZipPath -Force | Out-Null
    }
    exit 1
}

Write-Host "Unzip complete. Deleting temporary zip file..."
if (Test-Path $ZipPath) {
    Remove-Item -Path $ZipPath -Force | Out-Null
}

Write-Host "Data updated successfully in: $OutputDir"
