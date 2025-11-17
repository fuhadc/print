#!/bin/bash

# Setup script for Barcode Printer GUI

echo "=========================================="
echo "Thermal Printer Setup"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3 first"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed"
    echo "Please install pip3 first"
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Install requirements
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Dependencies installed successfully!"
    echo ""
    echo "=========================================="
    echo "Installation Complete!"
    echo "=========================================="
    echo ""
    echo "To run the GUI application:"
    echo "  python3 barcode_printer_gui.py"
    echo ""
    echo "To run the CLI badge printer:"
    echo "  python3 print-badge.py 'Line 1' 'Line 2'"
    echo ""
    echo "To see examples:"
    echo "  python3 example_usage.py"
    echo ""
else
    echo ""
    echo "❌ Error: Failed to install dependencies"
    echo "Please check the error messages above"
    exit 1
fi


