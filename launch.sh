#!/bin/bash

# Launch script for InsightHub

# Function to check if pip is installed
check_pip() {
    if ! command -v pip &> /dev/null; then
        echo "pip not found. Installing pip..."
        sudo apt update && sudo apt install -y python3-pip
        return 1  # Return 1 to indicate that something was installed
    fi
    return 0  # Return 0 to indicate everything is good
}

# Function to check if a package is installed
check_package_installed() {
    pip show "$1" &> /dev/null
    return $?  # Return the exit status of pip show
}

# Function to check required packages
check_packages() {
    local packages=("PyQt5" "PyQt6")  # Add other packages if needed
    for package in "${packages[@]}"; do
        if ! check_package_installed "$package"; then
            return 1  # Indicate that a package is missing
        fi
    done
    return 0  # Indicate everything is good
}

# Function to install requirements from requirements.txt
install_requirements() {
    if [ -f "requirements.txt" ]; then
        pip install --break-system-packages -r requirements.txt &> /dev/null
    fi
}

# Function to install PyQt5 and PyQt6
install_pyqt() {
    local packages=("PyQt5" "PyQt6")
    for package in "${packages[@]}"; do
        if ! check_package_installed "$package"; then
            echo "Installing $package..."
            pip install --break-system-packages "$package" &> /dev/null
        fi
    done
}

# Check if pip is installed
if ! check_pip; then
    echo "Please rerun the script after installing pip."
    exit 1
fi

# Check required packages
if ! check_packages; then
    echo "Installing missing packages..."
    install_pyqt
fi

# Check if requirements need to be installed
if [ -f "requirements.txt" ]; then
    echo "Skipping installation of dependencies as everything is good."
else
    echo "requirements.txt not found. Proceeding without installing dependencies."
fi

# Navigate to the src folder
if [ -d "src" ]; then
    cd src || { echo "Failed to change directory to src"; exit 1; }
else
    echo "Directory 'src' does not exist."
    exit 1
fi

# Run the main.py script without logging and suppress output
PYTHONWARNINGS="ignore::DeprecationWarning" python3 main.py &> /dev/null

# Check if the application started successfully
if [ $? -ne 0 ]; then
    echo "Failed to start InsightHub. Please check for errors."
    exit 1
fi

# Suppressed success message
# echo "InsightHub started successfully."

