# Project Overview: Thermal Printer Barcode Label System

## 📁 Project Structure

```
/Users/muhammedfuhadc/work/print/
│
├── 🎨 barcode_printer_gui.py     # Main GUI application
├── 🔧 print-badge.py              # CLI tool for simple badges
├── 📝 example_usage.py            # Usage examples and demos
│
├── ⚙️ setup.sh                    # Installation script
├── 📦 requirements.txt            # Python dependencies
├── 🙈 .gitignore                  # Git ignore file
│
├── 📖 README.md                   # Full documentation
├── 🚀 QUICKSTART.md              # Quick start guide
└── 📋 PROJECT_OVERVIEW.md        # This file
```

---

## 🎯 Main Components

### 1. **barcode_printer_gui.py** (21KB, 570+ lines)

The main GUI application with four key classes:

```python
┌─────────────────────────────────────┐
│     BarcodeConfig                   │  # Configuration storage
├─────────────────────────────────────┤
│  - Label dimensions                 │
│  - Barcode settings                 │
│  - Text settings                    │
│  - Print settings                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│     ThermalPrinter                  │  # Printer communication
├─────────────────────────────────────┤
│  - TSPL command generation          │
│  - Printer status checking          │
│  - Direct printer I/O               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│     BarcodePreview                  │  # Image generation
├─────────────────────────────────────┤
│  - PIL/Pillow integration           │
│  - Barcode image generation         │
│  - Preview rendering                │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│     BarcodePrinterGUI               │  # Main GUI
├─────────────────────────────────────┤
│  - Tkinter interface                │
│  - Real-time preview                │
│  - User input handling              │
└─────────────────────────────────────┘
```

**Features:**
- ✅ Visual label designer with live preview
- ✅ Multiple barcode formats (Code128, EAN13, etc.)
- ✅ Customizable dimensions and fonts
- ✅ Export to PNG/JPEG
- ✅ Direct thermal printer support
- ✅ Dry-run mode for testing

---

### 2. **print-badge.py** (5KB, 170+ lines)

Original CLI tool for simple two-line badges:

```bash
python3 print-badge.py "Line 1" "Line 2"
```

**Classes:**
- `Confirm` - Preview and confirmation
- `Badge` - Badge layout generation
- `Printer` - TSPL printer communication

**Features:**
- ✅ Command-line interface
- ✅ Text-only badges (no barcodes)
- ✅ Multiple copies support
- ✅ Orientation control
- ✅ Dry-run mode

---

### 3. **example_usage.py** (4.6KB)

Demonstrates programmatic usage with 5 examples:

1. **Basic Barcode** - Simple product label
2. **EAN13** - Retail barcode
3. **Asset Tag** - Equipment tracking
4. **Batch Printing** - Multiple labels
5. **Custom Sizes** - Various dimensions

Run it:
```bash
python3 example_usage.py
```

Generates preview images:
- `example1_basic_barcode.png`
- `example2_ean13.png`
- `example3_asset_tag.png`
- `example5_small_size.png`
- `example5_medium_size.png`
- `example5_large_size.png`

---

## 🔧 Dependencies

### Python Packages (requirements.txt)

```
python-barcode>=0.15.1   # Barcode generation
Pillow>=10.0.0           # Image processing
```

### Standard Library

- `tkinter` - GUI framework (included with Python)
- `os` - File and device I/O
- `sys` - System operations
- `time` - Timing and delays
- `re` - Regular expressions
- `argparse` - CLI parsing
- `io` - BytesIO for in-memory files

---

## 🏗️ Architecture

### Data Flow

```
User Input (GUI/CLI)
        ↓
  BarcodeConfig
        ↓
    ┌───┴───┐
    ↓       ↓
Preview   Printer
    ↓       ↓
  Image   TSPL Commands
    ↓       ↓
  Save    Thermal Print
```

### Printer Communication

```
Python → TSPL Commands → Thermal Printer
                ↓
        /dev/usb/lp0
        (or other device)
```

**TSPL Commands Used:**
- `SIZE` - Set label dimensions
- `GAP` - Set label gap
- `CODEPAGE` - Set character encoding
- `DIRECTION` - Set orientation
- `CLS` - Clear buffer
- `TEXT` - Print text
- `BARCODE` - Print barcode
- `PRINT` - Execute print job

---

## 🎨 GUI Layout

```
┌────────────────────────────────────────────────┐
│  Barcode Label Designer                        │
├──────────────────┬─────────────────────────────┤
│ Label Settings   │  Preview                    │
│ ┌──────────────┐ │  ┌───────────────────────┐  │
│ │ Barcode Data │ │  │                       │  │
│ │ Barcode Type │ │  │   [Label Preview]     │  │
│ │ Top Text     │ │  │                       │  │
│ │ Bottom Text  │ │  │                       │  │
│ └──────────────┘ │  └───────────────────────┘  │
│                  │                              │
│ Dimensions       │                              │
│ ┌──────────────┐ │                              │
│ │ Width        │ │                              │
│ │ Height       │ │                              │
│ │ Barcode H    │ │                              │
│ │ Bar Width    │ │                              │
│ │ Font Size    │ │                              │
│ └──────────────┘ │                              │
│                  │                              │
│ Print Settings   │                              │
│ ┌──────────────┐ │                              │
│ │ Copies       │ │                              │
│ │ Orientation  │ │                              │
│ │ Printer Dev  │ │                              │
│ └──────────────┘ │                              │
│                  │                              │
│ [Update Preview] │                              │
│ [Print] [Save]   │                              │
└──────────────────┴─────────────────────────────┘
```

---

## 📊 Supported Barcode Formats

| Format | Type | Length | Use Case |
|--------|------|--------|----------|
| Code128 | Alphanumeric | Variable | General purpose, shipping |
| Code39 | Alphanumeric | Variable | Legacy systems, asset tags |
| EAN13 | Numeric | 13 digits | Retail products (Europe) |
| EAN8 | Numeric | 8 digits | Small retail items |
| UPCA | Numeric | 12 digits | Retail products (USA) |

---

## 🎯 Use Cases

### 1. **Retail Product Labels**
- EAN13/UPCA barcodes
- Product name and price
- 100mm × 50mm labels

### 2. **Asset Tracking**
- Code128 alphanumeric IDs
- Company name and warnings
- 75mm × 35mm labels

### 3. **Shipping Labels**
- Code128 tracking numbers
- Recipient info and handling instructions
- 100mm × 60mm labels

### 4. **Inventory Management**
- Sequential barcodes
- Location and item codes
- Various sizes

### 5. **Event Badges**
- Text-only or with QR codes
- Names and affiliations
- Customizable layouts

---

## 🔒 Security & Permissions

### File Access
- Reads/writes to current directory
- Creates preview images
- No network access required

### Device Access
- Requires read/write permission to printer device
- On Linux: `sudo chmod 666 /dev/usb/lp0`
- Safe dry-run mode for testing

---

## 🚀 Getting Started

### Quick Start (3 commands)

```bash
# 1. Install dependencies
./setup.sh

# 2. Run GUI
python3 barcode_printer_gui.py

# 3. Design and print!
```

### Advanced Usage

```python
# Import in your code
from barcode_printer_gui import BarcodeConfig, ThermalPrinter

# Create configuration
config = BarcodeConfig()
config.barcode_data = "123456789012"
config.width_mm = 100
config.height_mm = 50

# Print
printer = ThermalPrinter('/dev/usb/lp0')
printer.print_barcode(config)
printer.close()
```

---

## 🐛 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| Printer not found | Check device path, verify connection |
| Barcode error | Check data format for barcode type |
| Preview blank | Click "Update Preview" button |
| Import error | Run `pip install -r requirements.txt` |
| Permission denied | Use `sudo` or change device permissions |

### Debug Mode

Enable dry-run mode to see TSPL commands without printing:
```python
printer = ThermalPrinter('/dev/usb/lp0', dry_run=True)
```

---

## 📈 Future Enhancements

Potential features to add:
- [ ] QR code support
- [ ] Logo/image insertion
- [ ] Database integration
- [ ] Network printer support
- [ ] Multi-page labels
- [ ] Template system
- [ ] Batch import from CSV
- [ ] Label designer presets

---

## 📝 License & Credits

- **License**: MIT (free to use and modify)
- **Based on**: [gelin's print-badge script](https://gist.github.com/gelin/7eea3132b029f8ac743010507abaab26)
- **Barcode Library**: python-barcode
- **GUI Framework**: tkinter (Python standard library)

---

## 📚 Documentation Files

1. **README.md** - Complete documentation with all features
2. **QUICKSTART.md** - Get started in minutes
3. **PROJECT_OVERVIEW.md** - This file, technical overview
4. **Code comments** - Inline documentation in source files

---

## 🎓 Learning Resources

### Understanding TSPL
- TSC Printer Language for thermal printers
- Text-based command protocol
- Commands sent via serial/USB device

### Python Libraries Used
- **tkinter**: Standard GUI library
- **python-barcode**: Barcode generation
- **Pillow (PIL)**: Image processing
- **os/sys**: System interaction

### Thermal Printing
- Direct thermal vs. thermal transfer
- Label stock sizes and materials
- Dots per inch (DPI) resolution
- Roll vs. die-cut labels

---

**Project Created**: November 16, 2024
**Python Version**: 3.x
**Platform**: Cross-platform (Linux, macOS, Windows with modifications)


