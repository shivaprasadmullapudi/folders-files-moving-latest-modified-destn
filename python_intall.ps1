# Check if Chocolatey is installed; if not, install it.
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Chocolatey is not installed. Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
} else {
    Write-Host "Chocolatey is already installed."
}

# Install Python using Chocolatey (this installs the latest stable Python)
Write-Host "Installing Python..."
choco install python -y

# Verify Python installation
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "Python has been installed successfully."
} else {
    Write-Host "There was an issue installing Python."
}
