# Thermal Printer Barcode Label Generator

A GUI application for designing and printing barcode labels to TSC thermal printers using TSPL (TSC Printer Language).

## Features

- 🎨 **Visual Label Designer** - Real-time preview of your labels
- 🏷️ **Barcode Generation** - Support for multiple barcode formats (Code128, Code39, EAN13, EAN8, UPCA)
- 📐 **Customizable Dimensions** - Adjust label width, height, barcode size
- ✏️ **Text Labels** - Add custom text above and below barcodes
- 🖨️ **Direct Printing** - Print directly to TSC thermal printers
- 💾 **Export Images** - Save label designs as PNG/JPEG files
- 🔄 **Batch Printing** - Print multiple copies at once

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install python-barcode Pillow
```

### 2. Configure Printer

Edit the printer device path in the GUI or in the code:
- **Linux**: `/dev/usb/lp0` or `/dev/ttyUSB0`
- **macOS**: `/dev/cu.usbserial` or similar
- **Windows**: `COM3` or similar port

## Usage

### Running the GUI Application

```bash
python3 barcode_printer_gui.py
```

### GUI Controls

#### Label Settings
- **Barcode Data**: The data to encode (numbers/text)
- **Barcode Type**: Choose from Code128, Code39, EAN13, etc.
- **Top Text**: Text displayed above the barcode
- **Bottom Text**: Text displayed below the barcode

#### Dimensions
- **Label Width**: Total label width in millimeters (30-200mm)
- **Label Height**: Total label height in millimeters (20-150mm)
- **Barcode Height**: Height of barcode bars in millimeters (5-50mm)
- **Bar Width**: Width multiplier for barcode bars (1-5)
- **Font Size**: Text font size in points (12-72)

#### Print Settings
- **Copies**: Number of labels to print (1-100)
- **Orientation**: Normal (human-readable) or Rotated (paper-efficient)
- **Printer Device**: Path to your thermal printer device

### Buttons
- **Update Preview**: Manually refresh the preview (auto-updates as you type)
- **Print**: Send the label to the thermal printer
- **Save Image**: Export the label design as an image file

## Running the Original CLI Tool

The original command-line badge printer is also included:

```bash
# Print a two-line badge
python3 print-badge.py "Line 1 Text" "Line 2 Text"

# Print 5 copies without confirmation
python3 print-badge.py -y -n 5 "HELLO" "WORLD"

# Dry run (preview commands without printing)
python3 print-badge.py -d "Test" "Badge"
```

## Supported Barcode Types

- **Code128**: Best for general alphanumeric data
- **Code39**: Older standard, alphanumeric
- **EAN13**: European Article Number (13 digits)
- **EAN8**: Shorter European Article Number (8 digits)
- **UPCA**: Universal Product Code (12 digits)

## Printer Configuration

The application works with TSC thermal printers that support TSPL commands:
- TSC TTP-244 Plus
- TSC TTP-345
- TSC TDP-225
- And other TSC TSPL-compatible printers

### Default Settings
- **Resolution**: 203 DPI (8 dots/mm)
- **Default Label**: 100mm × 50mm
- **Gap**: 2mm between labels

## Troubleshooting

### Printer Not Found
- Check printer device path
- Verify printer is connected and powered on
- On Linux, ensure you have permissions: `sudo chmod 666 /dev/usb/lp0`
- Use dry-run mode to test without a printer

### Barcode Not Generating
- Verify barcode data matches the format requirements:
  - **EAN13**: Exactly 12 digits (13th is checksum)
  - **EAN8**: Exactly 7 digits (8th is checksum)
  - **UPCA**: Exactly 11 digits (12th is checksum)
  - **Code128/Code39**: Alphanumeric data

### Preview Not Showing
- Ensure Pillow is installed: `pip install Pillow`
- Try clicking "Update Preview" button

## Examples

### Example 1: Product Label
```
Barcode Data: 123456789012
Top Text: PREMIUM COFFEE
Bottom Text: Organic Blend
Label: 100mm × 50mm
```

### Example 2: Asset Tag
```
Barcode Data: ASSET-2024-001
Barcode Type: Code128
Top Text: COMPANY NAME
Bottom Text: DO NOT REMOVE
Label: 75mm × 35mm
```

### Example 3: Shipping Label
```
Barcode Data: 4901234567890
Barcode Type: EAN13
Top Text: (empty)
Bottom Text: FRAGILE
Label: 100mm × 60mm
```

## License

MIT License - Feel free to modify and use for your projects.

## Credits

Based on the thermal printer script by [@gelin](https://gist.github.com/gelin/7eea3132b029f8ac743010507abaab26)


