# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
./setup.sh
```

Or manually:
```bash
pip3 install python-barcode Pillow
```

### Step 2: Run the GUI

```bash
python3 barcode_printer_gui.py
```

### Step 3: Design Your Label

1. **Enter barcode data** (e.g., "123456789012")
2. **Add text** (optional top and bottom text)
3. **Adjust dimensions** to fit your label size
4. **Click "Update Preview"** to see your design
5. **Click "Print"** when ready!

---

## 📸 Screenshot Guide

### Main Interface

```
┌─────────────────────────────────────────────────────┐
│  Thermal Printer - Barcode Label Generator         │
├──────────────────┬──────────────────────────────────┤
│  Label Settings  │         Preview                  │
│                  │                                  │
│  Barcode Data:   │    ┌────────────────────┐       │
│  [123456789012]  │    │   PRODUCT NAME     │       │
│                  │    │   |||||||||||||||   │       │
│  Top Text:       │    │   123456789012     │       │
│  [PRODUCT NAME]  │    │   Made in USA      │       │
│                  │    └────────────────────┘       │
│  Bottom Text:    │                                  │
│  [Made in USA]   │                                  │
│                  │                                  │
│  Width: 100 mm   │                                  │
│  Height: 50 mm   │                                  │
│                  │                                  │
│  [Update] [Print]│                                  │
└──────────────────┴──────────────────────────────────┘
```

---

## 🏷️ Common Label Examples

### Example 1: Product Label
```
Barcode: 123456789012
Type: Code128
Top: "ORGANIC COFFEE"
Bottom: "$12.99"
Size: 100mm × 50mm
```

### Example 2: Asset Tag
```
Barcode: ASSET-2024-001
Type: Code128
Top: "COMPANY NAME"
Bottom: "DO NOT REMOVE"
Size: 75mm × 35mm
```

### Example 3: Shipping Label
```
Barcode: 590123412345
Type: EAN13
Top: (empty)
Bottom: "FRAGILE - HANDLE WITH CARE"
Size: 100mm × 60mm
```

---

## ⚙️ Quick Settings Reference

### Label Dimensions
- **Width**: 30-200mm (most common: 100mm)
- **Height**: 20-150mm (most common: 50mm)
- **Barcode Height**: 5-50mm (recommended: 12-15mm)

### Barcode Types
- **Code128**: Best for alphanumeric (letters + numbers)
- **Code39**: Older standard, less compact
- **EAN13**: Retail products (13 digits)
- **EAN8**: Smaller retail items (8 digits)
- **UPCA**: North American retail (12 digits)

### Font Sizes
- **Small labels**: 16-20pt
- **Medium labels**: 24-28pt
- **Large labels**: 32-40pt

---

## 🖨️ Printer Setup

### Finding Your Printer

**Linux:**
```bash
ls /dev/usb/lp*
ls /dev/ttyUSB*
```

**macOS:**
```bash
ls /dev/cu.*
```

**Windows:**
- Check Device Manager for COM port

### Testing Without a Printer

Don't have a printer connected? No problem!

1. Enter a non-existent device path
2. The app will run in **DRY-RUN mode**
3. Commands will print to the console
4. You can still save images!

---

## 💡 Tips & Tricks

### 1. Live Preview
- Preview updates automatically as you type
- Wait 0.5 seconds after typing for update

### 2. Save Designs
- Click "Save Image" to export as PNG
- Use 300 DPI for high-quality prints

### 3. Batch Printing
- Set "Copies" to print multiple labels
- Each copy is identical

### 4. Orientation
- **Normal (1)**: Human-readable orientation
- **Rotated (0)**: Paper-efficient for continuous rolls

### 5. Common Issues

**Barcode won't generate?**
- Check data format (EAN13 needs 12 digits exactly)
- Try Code128 for mixed text/numbers

**Preview looks blurry?**
- This is just the preview scaling
- Actual print will be sharp!

**Printer not responding?**
- Check power and connection
- Verify device path is correct
- Try dry-run mode first

---

## 🎯 Next Steps

### Run Examples
```bash
python3 example_usage.py
```
This will generate sample labels showing different configurations.

### Use CLI Tool
For simple two-line badges without barcodes:
```bash
python3 print-badge.py "Hello" "World"
```

### Programmatic Usage
Import the classes in your own Python scripts:
```python
from barcode_printer_gui import BarcodeConfig, ThermalPrinter, BarcodePreview

config = BarcodeConfig()
config.barcode_data = "123456789012"
# ... configure other settings

preview = BarcodePreview.generate(config)
preview.save("my_label.png")
```

---

## 📚 More Information

- See **README.md** for detailed documentation
- See **example_usage.py** for code examples
- Check the source code for customization options

---

## ❓ Need Help?

Common questions:

**Q: Can I use this without a thermal printer?**  
A: Yes! Use the "Save Image" feature to export labels as images.

**Q: What printers are supported?**  
A: Any TSC thermal printer that supports TSPL commands.

**Q: Can I add logos or images?**  
A: Not in the current version, but the code is extensible!

**Q: Can I change colors?**  
A: Thermal printers only print in black. Preview shows black on white.

---

**Happy Printing! 🎉**


