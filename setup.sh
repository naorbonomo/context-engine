#!/bin/bash

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BLUE='\033[0;34m'

# Function to print status messages
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

# Function to print error messages
print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Function to print warning messages
print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Function to check if a command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        print_error "$1 is not installed"
        return 1
    fi
    return 0
}

# Function to check if a port is available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        print_error "Port $1 is already in use"
        return 1
    fi
    return 0
}

# Function to check if virtual environment is properly set up
check_venv() {
    if [ -d "backend/.venv" ] && [ -f "backend/.venv/bin/activate" ]; then
        source backend/.venv/bin/activate
        if pip freeze | grep -q "fastapi" && pip freeze | grep -q "uvicorn"; then
            return 0  # venv exists and has required packages
        fi
    fi
    return 1
}

# Function to setup Python environment
setup_python() {
    print_status "Setting up Python environment..."
    cd backend
    
    # Create virtual environment
    print_status "Creating virtual environment..."
    if [ -d ".venv" ]; then
        print_warning "Virtual environment already exists. Recreating..."
        rm -rf .venv
    fi
    python3.10 -m venv .venv
    print_success "Virtual environment created"

    # Activate virtual environment
    print_status "Activating virtual environment..."
    source .venv/bin/activate
    
    # Install requirements
    print_status "Installing Python requirements..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Python requirements installed"
    
    cd ..
}

# Function to start both frontend and backend
start_servers() {
    print_status "Starting both frontend and backend servers..."
    print_warning "Use Ctrl+C to stop the servers"
    echo ""

    # Store the original directory
    ORIGINAL_DIR=$(pwd)

    # Start frontend in background
    print_status "Starting frontend development server..."
    cd frontend && npm run dev &

    # Give frontend a moment to start
    sleep 2

    # Start backend using absolute paths
    print_status "Starting backend server..."
    cd "$ORIGINAL_DIR/backend"
    source .venv/bin/activate  # Make sure venv is activated
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Function to check backend setup
check_backend() {
    # First check if Python 3.10 exists
    if ! command -v python3.10 &> /dev/null; then
        print_warning "Python 3.10 not found"
        return 1
    fi

    # Then check venv and packages
    if [ -d "backend/.venv" ] && [ -f "backend/.venv/bin/activate" ]; then
        source backend/.venv/bin/activate
        if pip freeze | grep -q "fastapi" && pip freeze | grep -q "uvicorn"; then
            return 0  # Backend is fully set up
        fi
    fi
    return 1  # Backend needs setup
}

# Function to check frontend setup
check_frontend() {
    # First check if Node exists
    if ! command -v node &> /dev/null; then
        print_warning "Node.js not found"
        return 1
    fi

    # Then check node_modules
    if [ -d "frontend/node_modules" ]; then
        return 0  # Frontend is set up
    fi
    return 1  # Frontend needs setup
}

# Main setup function
main() {
    print_status "Starting Context Engine..."

    # 1. Check Backend
    if ! check_backend; then
        print_status "Setting up backend..."
        
        # Install Python if needed
        if ! command -v python3.10 &> /dev/null; then
            print_warning "Python 3.10 not found. Attempting to install..."
            
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS Python installation code
                print_status "Downloading Python 3.10 installer..."
                if [[ $(uname -m) == "arm64" ]]; then
                    curl -o python_installer.pkg "https://www.python.org/ftp/python/3.10.0/python-3.10.0-macos11.pkg"
                else
                    curl -o python_installer.pkg "https://www.python.org/ftp/python/3.10.0/python-3.10.0-macos11.pkg"
                fi
                
                print_status "Installing Python 3.10..."
                sudo installer -pkg python_installer.pkg -target /
                rm python_installer.pkg
                echo 'export PATH="/Library/Frameworks/Python.framework/Versions/3.10/bin:$PATH"' >> ~/.zshrc
                source ~/.zshrc
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                # Linux installation code
                if command -v apt &> /dev/null; then
                    print_status "Installing Python 3.10 via apt..."
                    sudo apt update
                    sudo apt install -y software-properties-common
                    sudo add-apt-repository -y ppa:deadsnakes/ppa
                    sudo apt install -y python3.10 python3.10-venv
                elif command -v dnf &> /dev/null; then
                    print_status "Installing Python 3.10 via dnf..."
                    sudo dnf install -y python3.10
                fi
            fi
        fi
        
        # Setup Python environment
        setup_python
    else
        print_success "Backend already set up"
    fi

    # 2. Check Frontend
    if ! check_frontend; then
        print_status "Setting up frontend..."
        if ! command -v node &> /dev/null; then
            print_error "Node.js is required but not found"
            print_warning "Please install Node.js from https://nodejs.org/"
            exit 1
        fi
        cd frontend
        npm install
        cd ..
    else
        print_success "Frontend already set up"
    fi

    # 3. Run both servers
    start_servers
}

# Execute main function
main
main