"""
Advanced Image Compressor
A comprehensive image compression tool with multiple algorithms and formats support.
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageOps
import numpy as np
import cv2
import customtkinter as ctk
from typing import List, Tuple, Optional
import threading
import time

class ImageCompressor:
    """Core image compression functionality"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        self.compression_methods = {
            'JPEG Quality': self._compress_jpeg,
            'PNG Optimization': self._compress_png,
            'WebP Conversion': self._compress_webp,
            'Size Reduction': self._compress_resize,
            'Advanced Lossy': self._compress_advanced_lossy
        }
    
    def compress_image(self, input_path: str, output_path: str, 
                      method: str = 'JPEG Quality', quality: int = 85, 
                      max_size: Tuple[int, int] = None) -> dict:
        """
        Compress an image using the specified method
        
        Args:
            input_path: Path to input image
            output_path: Path to save compressed image
            method: Compression method to use
            quality: Quality setting (1-100)
            max_size: Maximum dimensions (width, height)
            
        Returns:
            Dictionary with compression results
        """
        try:
            # Load image
            with Image.open(input_path) as img:
                original_size = os.path.getsize(input_path)
                original_format = img.format
                
                # Apply compression method
                if method in self.compression_methods:
                    compressed_img = self.compression_methods[method](
                        img, quality, max_size
                    )
                else:
                    compressed_img = self._compress_jpeg(img, quality, max_size)
                
                # Save compressed image
                compressed_img.save(output_path, optimize=True)
                compressed_size = os.path.getsize(output_path)
                
                # Calculate compression ratio
                compression_ratio = (1 - compressed_size / original_size) * 100
                
                return {
                    'success': True,
                    'original_size': original_size,
                    'compressed_size': compressed_size,
                    'compression_ratio': compression_ratio,
                    'original_format': original_format,
                    'output_format': compressed_img.format
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _compress_jpeg(self, img: Image.Image, quality: int, max_size: Tuple[int, int]) -> Image.Image:
        """Compress using JPEG quality reduction"""
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        if max_size:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        return img
    
    def _compress_png(self, img: Image.Image, quality: int, max_size: Tuple[int, int]) -> Image.Image:
        """Compress PNG using optimization"""
        if max_size:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary for better compression
        if img.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        
        return img
    
    def _compress_webp(self, img: Image.Image, quality: int, max_size: Tuple[int, int]) -> Image.Image:
        """Convert to WebP format"""
        if max_size:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        if img.mode in ('RGBA', 'LA'):
            pass  # Keep transparency
        elif img.mode == 'P':
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
        
        return img
    
    def _compress_resize(self, img: Image.Image, quality: int, max_size: Tuple[int, int]) -> Image.Image:
        """Compress by resizing"""
        if max_size:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert to RGB for JPEG compression
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        return img
    
    def _compress_advanced_lossy(self, img: Image.Image, quality: int, max_size: Tuple[int, int]) -> Image.Image:
        """Advanced lossy compression using OpenCV"""
        # Convert PIL to OpenCV format
        cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        if max_size:
            height, width = cv_img.shape[:2]
            max_w, max_h = max_size
            
            if width > max_w or height > max_h:
                scale = min(max_w/width, max_h/height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                cv_img = cv2.resize(cv_img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # Apply Gaussian blur for additional compression
        if quality < 70:
            kernel_size = max(1, int((100 - quality) / 20))
            if kernel_size % 2 == 0:
                kernel_size += 1
            cv_img = cv2.GaussianBlur(cv_img, (kernel_size, kernel_size), 0)
        
        # Convert back to PIL
        img = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
        
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        return img

class ImageCompressorGUI:
    """Modern GUI for the image compressor"""
    
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Advanced Image Compressor")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Initialize compressor
        self.compressor = ImageCompressor()
        
        # Variables
        self.input_files = []
        self.output_dir = ""
        self.compression_method = tk.StringVar(value="JPEG Quality")
        self.quality = tk.IntVar(value=85)
        self.max_width = tk.IntVar(value=1920)
        self.max_height = tk.IntVar(value=1080)
        self.batch_mode = tk.BooleanVar(value=False)
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Advanced Image Compressor",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # File selection frame
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(file_frame, text="Select Images:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # File selection buttons
        button_frame = ctk.CTkFrame(file_frame)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        self.select_files_btn = ctk.CTkButton(
            button_frame,
            text="Select Images",
            command=self.select_files,
            width=150
        )
        self.select_files_btn.pack(side="left", padx=10)
        
        self.select_folder_btn = ctk.CTkButton(
            button_frame,
            text="Select Folder",
            command=self.select_folder,
            width=150
        )
        self.select_folder_btn.pack(side="left", padx=10)
        
        # File list
        self.file_listbox = tk.Listbox(file_frame, height=6, font=("Arial", 10))
        self.file_listbox.pack(fill="x", padx=20, pady=10)
        
        # Scrollbar for file list
        scrollbar = tk.Scrollbar(file_frame, orient="vertical", command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Settings frame
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(settings_frame, text="Compression Settings:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Compression method
        method_frame = ctk.CTkFrame(settings_frame)
        method_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(method_frame, text="Method:").pack(side="left", padx=10)
        method_combo = ctk.CTkComboBox(
            method_frame,
            values=list(self.compressor.compression_methods.keys()),
            variable=self.compression_method,
            width=200
        )
        method_combo.pack(side="left", padx=10)
        
        # Quality setting
        quality_frame = ctk.CTkFrame(settings_frame)
        quality_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(quality_frame, text="Quality:").pack(side="left", padx=10)
        quality_slider = ctk.CTkSlider(
            quality_frame,
            from_=1,
            to=100,
            variable=self.quality,
            width=200
        )
        quality_slider.pack(side="left", padx=10)
        
        self.quality_label = ctk.CTkLabel(quality_frame, text="85")
        self.quality_label.pack(side="left", padx=10)
        
        # Update quality label when slider changes
        quality_slider.configure(command=self.update_quality_label)
        
        # Max dimensions
        size_frame = ctk.CTkFrame(settings_frame)
        size_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(size_frame, text="Max Width:").pack(side="left", padx=10)
        width_entry = ctk.CTkEntry(size_frame, textvariable=self.max_width, width=100)
        width_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(size_frame, text="Max Height:").pack(side="left", padx=10)
        height_entry = ctk.CTkEntry(size_frame, textvariable=self.max_height, width=100)
        height_entry.pack(side="left", padx=5)
        
        # Output directory
        output_frame = ctk.CTkFrame(main_frame)
        output_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(output_frame, text="Output Directory:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        output_button_frame = ctk.CTkFrame(output_frame)
        output_button_frame.pack(fill="x", padx=20, pady=10)
        
        self.select_output_btn = ctk.CTkButton(
            output_button_frame,
            text="Select Output Folder",
            command=self.select_output_dir,
            width=200
        )
        self.select_output_btn.pack(side="left", padx=10)
        
        self.output_label = ctk.CTkLabel(output_button_frame, text="No output directory selected")
        self.output_label.pack(side="left", padx=10)
        
        # Progress bar
        self.progress_frame = ctk.CTkFrame(main_frame)
        self.progress_frame.pack(fill="x", padx=20, pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=10)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Ready to compress")
        self.progress_label.pack(pady=5)
        
        # Compress button
        self.compress_btn = ctk.CTkButton(
            main_frame,
            text="Start Compression",
            command=self.start_compression,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.compress_btn.pack(pady=20)
        
        # Results text area
        self.results_text = tk.Text(main_frame, height=8, font=("Arial", 10))
        self.results_text.pack(fill="both", expand=True, padx=20, pady=10)
        
    def update_quality_label(self, value):
        """Update quality label when slider changes"""
        self.quality_label.configure(text=str(int(float(value))))
    
    def select_files(self):
        """Select individual image files"""
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
                ("All files", "*.*")
            ]
        )
        if files:
            self.input_files = list(files)
            self.update_file_list()
    
    def select_folder(self):
        """Select folder containing images"""
        folder = filedialog.askdirectory(title="Select Folder with Images")
        if folder:
            self.input_files = []
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in self.compressor.supported_formats):
                        self.input_files.append(os.path.join(root, file))
            self.update_file_list()
    
    def update_file_list(self):
        """Update the file list display"""
        self.file_listbox.delete(0, tk.END)
        for file in self.input_files:
            filename = os.path.basename(file)
            self.file_listbox.insert(tk.END, filename)
    
    def select_output_dir(self):
        """Select output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir = directory
            self.output_label.configure(text=f"Output: {os.path.basename(directory)}")
    
    def start_compression(self):
        """Start the compression process"""
        if not self.input_files:
            messagebox.showerror("Error", "Please select at least one image file.")
            return
        
        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return
        
        # Disable compress button during processing
        self.compress_btn.configure(state="disabled")
        
        # Start compression in a separate thread
        thread = threading.Thread(target=self.compress_images)
        thread.daemon = True
        thread.start()
    
    def compress_images(self):
        """Compress all selected images"""
        total_files = len(self.input_files)
        successful = 0
        failed = 0
        total_original_size = 0
        total_compressed_size = 0
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Starting compression...\n\n")
        
        for i, input_path in enumerate(self.input_files):
            try:
                # Update progress
                progress = (i + 1) / total_files
                self.root.after(0, lambda p=progress: self.progress_bar.set(p))
                self.root.after(0, lambda i=i, t=total_files: 
                    self.progress_label.configure(text=f"Processing {i+1}/{t}"))
                
                # Generate output filename
                filename = os.path.basename(input_path)
                name, ext = os.path.splitext(filename)
                
                # Determine output format based on compression method
                method = self.compression_method.get()
                if method == "WebP Conversion":
                    output_ext = ".webp"
                elif method == "PNG Optimization":
                    output_ext = ".png"
                else:
                    output_ext = ".jpg"
                
                output_filename = f"{name}_compressed{output_ext}"
                output_path = os.path.join(self.output_dir, output_filename)
                
                # Compress image
                result = self.compressor.compress_image(
                    input_path,
                    output_path,
                    method,
                    self.quality.get(),
                    (self.max_width.get(), self.max_height.get())
                )
                
                if result['success']:
                    successful += 1
                    total_original_size += result['original_size']
                    total_compressed_size += result['compressed_size']
                    
                    # Add result to text area
                    result_text = f"✓ {filename}\n"
                    result_text += f"  Original: {self.format_size(result['original_size'])}\n"
                    result_text += f"  Compressed: {self.format_size(result['compressed_size'])}\n"
                    result_text += f"  Compression: {result['compression_ratio']:.1f}%\n\n"
                    
                    self.root.after(0, lambda text=result_text: 
                        self.results_text.insert(tk.END, text))
                else:
                    failed += 1
                    error_text = f"✗ {filename} - Error: {result['error']}\n\n"
                    self.root.after(0, lambda text=error_text: 
                        self.results_text.insert(tk.END, text))
                
            except Exception as e:
                failed += 1
                error_text = f"✗ {filename} - Error: {str(e)}\n\n"
                self.root.after(0, lambda text=error_text: 
                    self.results_text.insert(tk.END, text))
        
        # Final results
        total_compression_ratio = 0
        if total_original_size > 0:
            total_compression_ratio = (1 - total_compressed_size / total_original_size) * 100
        
        final_text = f"\n=== COMPRESSION COMPLETE ===\n"
        final_text += f"Successful: {successful}\n"
        final_text += f"Failed: {failed}\n"
        final_text += f"Total original size: {self.format_size(total_original_size)}\n"
        final_text += f"Total compressed size: {self.format_size(total_compressed_size)}\n"
        final_text += f"Overall compression: {total_compression_ratio:.1f}%\n"
        
        self.root.after(0, lambda text=final_text: 
            self.results_text.insert(tk.END, text))
        
        # Re-enable compress button
        self.root.after(0, lambda: self.compress_btn.configure(state="normal"))
        self.root.after(0, lambda: self.progress_label.configure(text="Compression complete"))
    
    def format_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main function to run the application"""
    app = ImageCompressorGUI()
    app.run()

if __name__ == "__main__":
    main()
