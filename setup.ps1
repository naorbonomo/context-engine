# Color definitions for PowerShell
$RED = "`e[31m"
$GREEN = "`e[32m"
$YELLOW = "`e[33m"
$BLUE = "`e[34m"
$NC = "`e[0m"

# Function to print status messages
function Print-Status {
    param($message)
    Write-Host "$BLUE[*]$NC $message"
}

# Function to print success messages
function Print-Success {
    param($message)
    Write-Host "$GREEN[✓]$NC $message"
}

# Function to print error messages
function Print-Error {
    param($message)
    Write-Host "$RED[✗]$NC $message"
}

# Function to print warning messages
function Print-Warning {
    param($message)
    Write-Host "$YELLOW[!]$NC $message"
}

# Function to check if a command exists
function Check-Command {
    param($cmd)
    if (!(Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Print-Error "$cmd is not installed"
        return $false
    }
    return $true
}

# Function to check if a port is available
function Check-Port {
    param($port)
    $inUse = Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue
    if ($inUse) {
        Print-Error "Port $port is already in use"
        return $false
    }
    return $true
}

# Function to check if virtual environment is properly set up
function Check-Venv {
    if ((Test-Path "backend\.venv") -and (Test-Path "backend\.venv\Scripts\Activate.ps1")) {
        . backend\.venv\Scripts\Activate.ps1
        $packages = pip freeze
        if ($packages -match "fastapi" -and $packages -match "uvicorn") {
            return $true
        }
    }
    return $false
}

# Function to setup Python environment
function Setup-Python {
    Print-Status "Setting up Python environment..."
    Push-Location backend

    # Create virtual environment
    Print-Status "Creating virtual environment..."
    if (Test-Path ".venv") {
        Print-Warning "Virtual environment already exists. Recreating..."
        Remove-Item -Recurse -Force .venv
    }
    python -m venv .venv
    Print-Success "Virtual environment created"

    # Activate virtual environment
    Print-Status "Activating virtual environment..."
    . .venv\Scripts\Activate.ps1

    # Install requirements
    Print-Status "Installing Python requirements..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    Print-Success "Python requirements installed"

    Pop-Location
}

# Function to start both frontend and backend
function Start-Servers {
    Print-Status "Starting both frontend and backend servers..."
    Print-Warning "Use Ctrl+C to stop the servers"
    Write-Host ""

    # Store the original directory
    $originalDir = Get-Location

    # Start frontend in background
    Print-Status "Starting frontend development server..."
    Push-Location frontend
    Start-Process -NoNewWindow powershell -ArgumentList "npm run dev"
    Pop-Location

    # Give frontend a moment to start
    Start-Sleep -Seconds 2

    # Start backend
    Print-Status "Starting backend server..."
    Push-Location "$originalDir\backend"
    . .venv\Scripts\Activate.ps1
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Function to check backend setup
function Check-Backend {
    # Check if Python exists
    if (!(Get-Command python -ErrorAction SilentlyContinue)) {
        Print-Warning "Python not found"
        return $false
    }

    # Check venv and packages
    return Check-Venv
}

# Function to check frontend setup
function Check-Frontend {
    # Check if Node exists
    if (!(Get-Command node -ErrorAction SilentlyContinue)) {
        Print-Warning "Node.js not found"
        return $false
    }

    # Check node_modules
    if (Test-Path "frontend\node_modules") {
        return $true
    }
    return $false
}

# Main setup function
function Main {
    Print-Status "Starting Context Engine..."

    # 1. Check Backend
    if (!(Check-Backend)) {
        Print-Status "Setting up backend..."
        
        # Check Python installation
        if (!(Get-Command python -ErrorAction SilentlyContinue)) {
            Print-Warning "Python not found. Please install Python from https://www.python.org/"
            Print-Warning "Make sure to check 'Add Python to PATH' during installation"
            exit 1
        }
        
        # Setup Python environment
        Setup-Python
    }
    else {
        Print-Success "Backend already set up"
    }

    # 2. Check Frontend
    if (!(Check-Frontend)) {
        Print-Status "Setting up frontend..."
        if (!(Get-Command node -ErrorAction SilentlyContinue)) {
            Print-Error "Node.js is required but not found"
            Print-Warning "Please install Node.js from https://nodejs.org/"
            exit 1
        }
        Push-Location frontend
        npm install
        Pop-Location
    }
    else {
        Print-Success "Frontend already set up"
    }

    # 3. Run both servers
    Start-Servers
}

# Execute main function
Main 