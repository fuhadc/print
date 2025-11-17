#!/usr/bin/env python3
"""
Example usage of the barcode printer programmatically
"""

from barcode_printer_gui import BarcodeConfig, ThermalPrinter, BarcodePreview

def example_1_basic_barcode():
    """Example 1: Basic barcode label"""
    print("Example 1: Basic Barcode Label")
    print("-" * 50)
    
    config = BarcodeConfig()
    config.barcode_data = "123456789012"
    config.top_text = "PRODUCT NAME"
    config.bottom_text = "Made in USA"
    config.width_mm = 100
    config.height_mm = 50
    
    # Generate preview and save
    preview = BarcodePreview.generate(config)
    preview.save("example1_basic_barcode.png")
    print("✓ Preview saved as: example1_basic_barcode.png")
    
    # Print to thermal printer (dry run)
    printer = ThermalPrinter('/dev/usb/lp0', dry_run=True)
    print("\nTSPL Commands:")
    printer.print_barcode(config)
    printer.close()
    print()


def example_2_ean13_barcode():
    """Example 2: EAN13 barcode for retail"""
    print("Example 2: EAN13 Barcode")
    print("-" * 50)
    
    config = BarcodeConfig()
    config.barcode_type = 'ean13'
    config.barcode_data = "590123412345"  # 12 digits for EAN13
    config.top_text = "ORGANIC COFFEE"
    config.bottom_text = "$12.99"
    config.width_mm = 80
    config.height_mm = 40
    config.barcode_height = 12
    
    preview = BarcodePreview.generate(config)
    preview.save("example2_ean13.png")
    print("✓ Preview saved as: example2_ean13.png")
    print()


def example_3_asset_tag():
    """Example 3: Asset tracking label"""
    print("Example 3: Asset Tracking Label")
    print("-" * 50)
    
    config = BarcodeConfig()
    config.barcode_type = 'code128'
    config.barcode_data = "ASSET-2024-001"
    config.top_text = "ACME CORPORATION"
    config.bottom_text = "Property of ACME"
    config.width_mm = 75
    config.height_mm = 35
    config.barcode_height = 10
    config.font_size = 18
    
    preview = BarcodePreview.generate(config)
    preview.save("example3_asset_tag.png")
    print("✓ Preview saved as: example3_asset_tag.png")
    print()


def example_4_batch_printing():
    """Example 4: Batch print multiple labels"""
    print("Example 4: Batch Printing")
    print("-" * 50)
    
    # Generate multiple different labels
    labels = [
        {"data": "ITEM-001", "top": "Widget A", "bottom": "Aisle 1"},
        {"data": "ITEM-002", "top": "Widget B", "bottom": "Aisle 2"},
        {"data": "ITEM-003", "top": "Widget C", "bottom": "Aisle 3"},
    ]
    
    printer = ThermalPrinter('/dev/usb/lp0', dry_run=True)
    
    for i, label_data in enumerate(labels, 1):
        config = BarcodeConfig()
        config.barcode_data = label_data["data"]
        config.top_text = label_data["top"]
        config.bottom_text = label_data["bottom"]
        
        print(f"\nLabel {i}:")
        printer.print_barcode(config)
    
    printer.close()
    print("\n✓ Batch print complete")
    print()


def example_5_custom_sizes():
    """Example 5: Different label sizes"""
    print("Example 5: Custom Label Sizes")
    print("-" * 50)
    
    sizes = [
        {"name": "Small", "width": 50, "height": 30, "barcode_h": 8, "font": 16},
        {"name": "Medium", "width": 75, "height": 40, "barcode_h": 12, "font": 20},
        {"name": "Large", "width": 100, "height": 60, "barcode_h": 20, "font": 28},
    ]
    
    for size in sizes:
        config = BarcodeConfig()
        config.barcode_data = "SIZE-TEST"
        config.top_text = f"{size['name']} Label"
        config.bottom_text = f"{size['width']}×{size['height']}mm"
        config.width_mm = size['width']
        config.height_mm = size['height']
        config.barcode_height = size['barcode_h']
        config.font_size = size['font']
        
        preview = BarcodePreview.generate(config)
        preview.save(f"example5_{size['name'].lower()}_size.png")
        print(f"✓ {size['name']} label saved: {size['width']}mm × {size['height']}mm")
    
    print()


def main():
    """Run all examples"""
    print("=" * 50)
    print("BARCODE PRINTER - USAGE EXAMPLES")
    print("=" * 50)
    print()
    
    try:
        example_1_basic_barcode()
        example_2_ean13_barcode()
        example_3_asset_tag()
        example_4_batch_printing()
        example_5_custom_sizes()
        
        print("=" * 50)
        print("All examples completed successfully!")
        print("Check the generated PNG files for previews.")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()


