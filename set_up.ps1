# Set the virtual environment directory
$VENV_DIR = "C:\Users\varun\New Volume D\Projects\Books Store\myshop\base"


# Activate the virtual environment
Write-Host "Activating virtual environment..."
& "$VENV_DIR\Scripts\Activate.ps1"

# Check if activation was successful
if ($env:VIRTUAL_ENV) {
    Write-Host "Virtual environment activated: $env:VIRTUAL_ENV"
} else {
    Write-Host "Failed to activate virtual environment."
    exit 1
}

