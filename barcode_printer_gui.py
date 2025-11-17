#!/usr/bin/env python3

import os
import sys
import time
import re
import platform
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font as tkfont
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import io

# Printer configuration - platform-specific defaults
if platform.system() == 'Windows':
    # Windows: Use printer name or COM port
    # Examples: "Thermal Printer", "COM3", "LPT1"
    PRINTER = "Thermal Printer"  # Change to your printer name or COM port
else:
    # Linux/Unix: Use device path
    PRINTER = '/dev/usb/lp0'  # the printer device

DOTS_MM = 8  # printer dots per mm, 8 == 203 dpi


class BarcodeConfig:
    """Configuration for barcode and label settings"""
    def __init__(self):
        # Label dimensions
        self.width_mm = 100
        self.height_mm = 50
        self.gap_mm = 2
        
        # Barcode settings
        self.barcode_type = 'code128'
        self.barcode_height = 15  # mm
        self.barcode_width = 2  # bar width multiplier
        
        # Text settings
        self.font_size = 24
        self.top_text = ''
        self.bottom_text = ''
        self.barcode_data = ''
        
        # Print settings
        self.orientation = 1  # 1 = human-friendly, 0 = paper-friendly
        self.num_copies = 1


class ThermalPrinter:
    """Handles communication with thermal printer using TSPL"""
    
    def __init__(self, printer_path, dry_run=False):
        self.printer_path = printer_path
        self.dry_run = dry_run
        self.printer = None
        self.is_windows = platform.system() == 'Windows'
        self.is_com_port = False
        
        if not self.dry_run:
            try:
                if self.is_windows:
                    # Check if it's a COM port (e.g., COM1, COM2, COM3)
                    if printer_path.upper().startswith('COM'):
                        # For COM ports, we'd need pyserial, but for now use win32print
                        # Most thermal printers on Windows should be accessed by name
                        self.is_com_port = True
                        raise Exception("COM port access requires pyserial. Use printer name instead.")
                    else:
                        # Use Windows printer name - will use win32print if available
                        try:
                            import win32print
                            self.win32print = win32print
                            self.printer_handle = None
                        except ImportError:
                            raise Exception("For Windows printing, install pywin32: pip install pywin32")
                else:
                    # Linux/Unix: Use device file
                    self.printer = os.open(printer_path, os.O_RDWR)
            except Exception as e:
                raise Exception(f"Cannot open printer at {printer_path}: {e}")
    
    def printer_status(self):
        """Get printer status"""
        if self.dry_run:
            return '@@@@'
        if self.is_windows:
            # Windows: Status checking is limited, assume ready
            return '@@@@'
        os.write(self.printer, b"\x1B!S\r\n")
        status = os.read(self.printer, 8)
        return status[1:5].decode('ascii')
    
    def can_print(self):
        """Check if printer is ready"""
        if self.dry_run:
            return True
        if self.is_windows:
            # Windows: Assume printer is ready
            return True
        return re.fullmatch(r'[@BCFPW]@@@', self.printer_status()) is not None
    
    def wait_printer(self):
        """Wait for printer to be ready"""
        if self.dry_run:
            return
        
        if not self.can_print():
            print('Waiting for printer...', file=sys.stderr)
            time.sleep(0.5)
            while not self.can_print():
                time.sleep(1)
    
    def command(self, cmd):
        """Send command to printer"""
        if self.dry_run:
            print(cmd)
        else:
            if self.is_windows:
                # Windows: Collect commands and send as raw data
                if not hasattr(self, '_command_buffer'):
                    self._command_buffer = []
                self._command_buffer.append(cmd + '\r\n')
            else:
                # Linux/Unix: Send directly to device
                os.write(self.printer, cmd.encode('utf-8'))
                os.write(self.printer, b'\r\n')
    
    def setup_page(self, config):
        """Setup page dimensions and settings"""
        # Initialize command buffer for Windows
        if self.is_windows and not self.dry_run:
            if not hasattr(self, '_command_buffer'):
                self._command_buffer = []
        
        self.command(f'SIZE {config.width_mm} mm,{config.height_mm} mm')
        self.command(f'GAP {config.gap_mm} mm,0 mm')
        self.command('CODEPAGE UTF-8')
        self.command(f'DIRECTION {config.orientation}')
        self.command('CLS')
    
    def print_barcode(self, config):
        """Print barcode label"""
        self.wait_printer()
        self.setup_page(config)
        
        width_dots = config.width_mm * DOTS_MM
        height_dots = config.height_mm * DOTS_MM
        x_center = width_dots // 2
        
        y_pos = 10  # Start position
        
        # Print top text if present
        if config.top_text:
            self.command(f'TEXT {x_center},{y_pos},"0",0,{config.font_size},{config.font_size},2,"{config.top_text}"')
            y_pos += config.font_size + 10
        
        # Print barcode
        if config.barcode_data:
            barcode_height_dots = config.barcode_height * DOTS_MM
            self.command(f'BARCODE {x_center},{y_pos},"128",{barcode_height_dots},1,0,{config.barcode_width},2,"{config.barcode_data}"')
            y_pos += barcode_height_dots + 20
        
        # Print bottom text if present
        if config.bottom_text:
            self.command(f'TEXT {x_center},{y_pos},"0",0,{config.font_size},{config.font_size},2,"{config.bottom_text}"')
        
        # Print the label
        self.command(f'PRINT 1,{config.num_copies}')
        
        # On Windows, flush all commands to printer
        if self.is_windows and not self.dry_run and hasattr(self, '_command_buffer'):
            self._flush_commands()
    
    def _flush_commands(self):
        """Send buffered commands to Windows printer"""
        if not hasattr(self, '_command_buffer') or not self._command_buffer:
            return
        
        try:
            # Get printer handle
            printer_handle = self.win32print.OpenPrinter(self.printer_path)
            try:
                # Start a print job
                job_info = self.win32print.StartDocPrinter(printer_handle, 1, ("TSPL Print Job", None, "RAW"))
                try:
                    self.win32print.StartPagePrinter(printer_handle)
                    
                    # Send all buffered commands
                    all_commands = ''.join(self._command_buffer).encode('utf-8')
                    self.win32print.WritePrinter(printer_handle, all_commands)
                    
                    self.win32print.EndPagePrinter(printer_handle)
                finally:
                    self.win32print.EndDocPrinter(printer_handle)
            finally:
                self.win32print.ClosePrinter(printer_handle)
            
            # Clear buffer
            self._command_buffer = []
        except Exception as e:
            raise Exception(f"Failed to send data to Windows printer: {e}")
    
    def close(self):
        """Close printer connection"""
        if self.is_windows:
            # Windows: Commands are already sent via win32print
            if hasattr(self, '_command_buffer'):
                self._command_buffer = []
        elif self.printer is not None:
            os.close(self.printer)


class BarcodePreview:
    """Generate preview image of barcode label"""
    
    @staticmethod
    def generate(config, dpi=203):
        """Generate PIL Image preview of the label"""
        # Convert mm to pixels at given DPI
        px_per_mm = dpi / 25.4
        width_px = int(config.width_mm * px_per_mm)
        height_px = int(config.height_mm * px_per_mm)
        
        # Create white background
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (width_px, height_px), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw border
        draw.rectangle([(0, 0), (width_px-1, height_px-1)], outline='black', width=2)
        
        y_pos = 20
        
        # Try to use a nice font, fall back to default
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", config.font_size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", config.font_size)
            except:
                font = ImageFont.load_default()
        
        # Draw top text
        if config.top_text:
            bbox = draw.textbbox((0, 0), config.top_text, font=font)
            text_width = bbox[2] - bbox[0]
            x_pos = (width_px - text_width) // 2
            draw.text((x_pos, y_pos), config.top_text, fill='black', font=font)
            y_pos += config.font_size + 20
        
        # Generate and draw barcode
        if config.barcode_data:
            try:
                # Generate barcode
                barcode_class = barcode.get_barcode_class(config.barcode_type)
                barcode_instance = barcode_class(config.barcode_data, writer=ImageWriter())
                
                # Generate barcode image in memory
                buffer = io.BytesIO()
                options = {
                    'module_height': config.barcode_height,
                    'module_width': config.barcode_width * 0.5,
                    'quiet_zone': 2,
                    'font_size': 0,  # Don't show text in barcode
                    'text_distance': 2,
                }
                barcode_instance.write(buffer, options=options)
                buffer.seek(0)
                
                # Load and resize barcode image
                barcode_img = Image.open(buffer)
                barcode_width = int(width_px * 0.8)
                aspect_ratio = barcode_img.height / barcode_img.width
                barcode_height = int(barcode_width * aspect_ratio)
                barcode_img = barcode_img.resize((barcode_width, barcode_height), Image.Resampling.LANCZOS)
                
                # Paste barcode centered
                x_barcode = (width_px - barcode_width) // 2
                img.paste(barcode_img, (x_barcode, y_pos))
                y_pos += barcode_height + 10
                
            except Exception as e:
                # If barcode generation fails, show error text
                error_text = f"Barcode Error: {str(e)}"
                draw.text((10, y_pos), error_text, fill='red', font=font)
                y_pos += config.font_size + 10
        
        # Draw bottom text
        if config.bottom_text:
            bbox = draw.textbbox((0, 0), config.bottom_text, font=font)
            text_width = bbox[2] - bbox[0]
            x_pos = (width_px - text_width) // 2
            draw.text((x_pos, y_pos), config.bottom_text, fill='black', font=font)
        
        return img


class BarcodePrinterGUI:
    """Main GUI application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Thermal Printer - Barcode Label Generator")
        self.root.geometry("900x700")
        
        self.config = BarcodeConfig()
        self.preview_image = None
        
        self.setup_ui()
        self.update_preview()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Barcode Label Designer", 
                               font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel - Controls
        controls_frame = ttk.LabelFrame(main_frame, text="Label Settings", padding="10")
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        row = 0
        
        # Barcode Data
        ttk.Label(controls_frame, text="Barcode Data:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.barcode_data_var = tk.StringVar(value="123456789012")
        ttk.Entry(controls_frame, textvariable=self.barcode_data_var, width=25).grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Barcode Type
        ttk.Label(controls_frame, text="Barcode Type:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.barcode_type_var = tk.StringVar(value="code128")
        barcode_types = ['code128', 'code39', 'ean13', 'ean8', 'upca']
        ttk.Combobox(controls_frame, textvariable=self.barcode_type_var, 
                    values=barcode_types, state='readonly', width=22).grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Top Text
        ttk.Label(controls_frame, text="Top Text:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.top_text_var = tk.StringVar(value="PRODUCT NAME")
        ttk.Entry(controls_frame, textvariable=self.top_text_var, width=25).grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Bottom Text
        ttk.Label(controls_frame, text="Bottom Text:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.bottom_text_var = tk.StringVar(value="Made in USA")
        ttk.Entry(controls_frame, textvariable=self.bottom_text_var, width=25).grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Separator
        ttk.Separator(controls_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        # Dimensions section
        ttk.Label(controls_frame, text="Dimensions (mm)", 
                 font=('Helvetica', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Label Width
        ttk.Label(controls_frame, text="Label Width:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.width_var = tk.IntVar(value=100)
        ttk.Spinbox(controls_frame, from_=30, to=200, textvariable=self.width_var, 
                   width=23).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Label Height
        ttk.Label(controls_frame, text="Label Height:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.height_var = tk.IntVar(value=50)
        ttk.Spinbox(controls_frame, from_=20, to=150, textvariable=self.height_var, 
                   width=23).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Barcode Height
        ttk.Label(controls_frame, text="Barcode Height:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.barcode_height_var = tk.IntVar(value=15)
        ttk.Spinbox(controls_frame, from_=5, to=50, textvariable=self.barcode_height_var, 
                   width=23).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Barcode Width (bar width)
        ttk.Label(controls_frame, text="Bar Width:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.barcode_width_var = tk.IntVar(value=2)
        ttk.Spinbox(controls_frame, from_=1, to=5, textvariable=self.barcode_width_var, 
                   width=23).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Font Size
        ttk.Label(controls_frame, text="Font Size:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.font_size_var = tk.IntVar(value=24)
        ttk.Spinbox(controls_frame, from_=12, to=72, textvariable=self.font_size_var, 
                   width=23).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Separator
        ttk.Separator(controls_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        # Print Settings
        ttk.Label(controls_frame, text="Print Settings", 
                 font=('Helvetica', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Number of Copies
        ttk.Label(controls_frame, text="Copies:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.copies_var = tk.IntVar(value=1)
        ttk.Spinbox(controls_frame, from_=1, to=100, textvariable=self.copies_var, 
                   width=23).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Orientation
        ttk.Label(controls_frame, text="Orientation:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.orientation_var = tk.IntVar(value=1)
        orient_frame = ttk.Frame(controls_frame)
        orient_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Radiobutton(orient_frame, text="Normal", variable=self.orientation_var, 
                       value=1).pack(side=tk.LEFT)
        ttk.Radiobutton(orient_frame, text="Rotated", variable=self.orientation_var, 
                       value=0).pack(side=tk.LEFT, padx=(10, 0))
        row += 1
        
        # Printer Path
        printer_label_text = "Printer Device:" if platform.system() != 'Windows' else "Printer Name:"
        help_text = " (e.g., /dev/usb/lp0)" if platform.system() != 'Windows' else " (e.g., Thermal Printer)"
        ttk.Label(controls_frame, text=printer_label_text + help_text).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.printer_path_var = tk.StringVar(value=PRINTER)
        ttk.Entry(controls_frame, textvariable=self.printer_path_var, width=25).grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Update Preview", 
                  command=self.update_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Print", 
                  command=self.print_label, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Image", 
                  command=self.save_preview).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Preview
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(preview_frame, bg='white', 
                                       width=400, height=500, relief=tk.SUNKEN, bd=2)
        self.preview_canvas.pack(expand=True, fill=tk.BOTH)
        
        # Bind variables to auto-update preview
        for var in [self.barcode_data_var, self.barcode_type_var, self.top_text_var, 
                   self.bottom_text_var, self.width_var, self.height_var, 
                   self.barcode_height_var, self.barcode_width_var, self.font_size_var]:
            var.trace_add('write', lambda *args: self.schedule_preview_update())
        
        self.preview_update_id = None
    
    def schedule_preview_update(self):
        """Schedule preview update with debounce"""
        if self.preview_update_id:
            self.root.after_cancel(self.preview_update_id)
        self.preview_update_id = self.root.after(500, self.update_preview)
    
    def get_config_from_ui(self):
        """Get configuration from UI inputs"""
        config = BarcodeConfig()
        config.barcode_data = self.barcode_data_var.get()
        config.barcode_type = self.barcode_type_var.get()
        config.top_text = self.top_text_var.get()
        config.bottom_text = self.bottom_text_var.get()
        config.width_mm = self.width_var.get()
        config.height_mm = self.height_var.get()
        config.barcode_height = self.barcode_height_var.get()
        config.barcode_width = self.barcode_width_var.get()
        config.font_size = self.font_size_var.get()
        config.num_copies = self.copies_var.get()
        config.orientation = self.orientation_var.get()
        return config
    
    def update_preview(self):
        """Update the preview image"""
        try:
            config = self.get_config_from_ui()
            
            # Generate preview image
            preview_img = BarcodePreview.generate(config)
            
            # Resize to fit canvas
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            if canvas_width < 50:  # Canvas not yet rendered
                canvas_width = 400
                canvas_height = 500
            
            # Calculate scaling to fit canvas
            img_ratio = preview_img.width / preview_img.height
            canvas_ratio = canvas_width / canvas_height
            
            if img_ratio > canvas_ratio:
                # Image is wider, fit to width
                new_width = int(canvas_width * 0.9)
                new_height = int(new_width / img_ratio)
            else:
                # Image is taller, fit to height
                new_height = int(canvas_height * 0.9)
                new_width = int(new_height * img_ratio)
            
            preview_img = preview_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.preview_image = ImageTk.PhotoImage(preview_img)
            
            # Display on canvas
            self.preview_canvas.delete("all")
            x = (canvas_width - new_width) // 2
            y = (canvas_height - new_height) // 2
            self.preview_canvas.create_image(x, y, anchor=tk.NW, image=self.preview_image)
            
        except Exception as e:
            messagebox.showerror("Preview Error", f"Failed to generate preview:\n{str(e)}")
    
    def save_preview(self):
        """Save preview image to file"""
        try:
            config = self.get_config_from_ui()
            preview_img = BarcodePreview.generate(config, dpi=300)
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            
            if filename:
                preview_img.save(filename)
                messagebox.showinfo("Success", f"Image saved to:\n{filename}")
        
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save image:\n{str(e)}")
    
    def print_label(self):
        """Print the label to thermal printer"""
        try:
            config = self.get_config_from_ui()
            printer_path = self.printer_path_var.get()
            
            # Ask for confirmation
            result = messagebox.askyesno(
                "Confirm Print",
                f"Print {config.num_copies} label(s) to:\n{printer_path}?"
            )
            
            if not result:
                return
            
            # Check if running in dry-run mode
            if platform.system() == 'Windows':
                # Windows: Check if printer exists by trying to open it
                try:
                    import win32print
                    printers = [p[2] for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)]
                    dry_run = printer_path not in printers
                except ImportError:
                    # If win32print not available, assume dry run
                    dry_run = True
                except:
                    # If check fails, assume dry run
                    dry_run = True
            else:
                # Linux/Unix: Check if device file exists
                dry_run = not os.path.exists(printer_path)
            
            if dry_run:
                messagebox.showwarning(
                    "Dry Run Mode",
                    f"Printer device not found at:\n{printer_path}\n\n"
                    "Running in DRY-RUN mode.\nCommands will be printed to console."
                )
            
            # Print
            printer = ThermalPrinter(printer_path, dry_run=dry_run)
            printer.print_barcode(config)
            printer.close()
            
            if not dry_run:
                messagebox.showinfo("Success", "Label sent to printer!")
            else:
                messagebox.showinfo("Dry Run Complete", 
                                   "Check console for TSPL commands.")
        
        except Exception as e:
            messagebox.showerror("Print Error", f"Failed to print:\n{str(e)}")


def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Style configuration
    style = ttk.Style()
    style.theme_use('default')
    
    app = BarcodePrinterGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

