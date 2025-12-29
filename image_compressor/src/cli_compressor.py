"""
Command Line Interface for Image Compressor
"""

import argparse
import os
import sys
from pathlib import Path
from image_compressor import ImageCompressor

def main():
    parser = argparse.ArgumentParser(description='Advanced Image Compressor CLI')
    parser.add_argument('input', help='Input image file or directory')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('-m', '--method', default='JPEG Quality', 
                       choices=['JPEG Quality', 'PNG Optimization', 'WebP Conversion', 
                               'Size Reduction', 'Advanced Lossy'],
                       help='Compression method')
    parser.add_argument('-q', '--quality', type=int, default=85, 
                       help='Quality setting (1-100)')
    parser.add_argument('--max-width', type=int, default=1920, 
                       help='Maximum width')
    parser.add_argument('--max-height', type=int, default=1080, 
                       help='Maximum height')
    parser.add_argument('--recursive', action='store_true', 
                       help='Process directories recursively')
    
    args = parser.parse_args()
    
    compressor = ImageCompressor()
    
    # Get input files
    input_files = []
    if os.path.isfile(args.input):
        input_files = [args.input]
    elif os.path.isdir(args.input):
        for root, dirs, files in os.walk(args.input):
            for file in files:
                if any(file.lower().endswith(ext) for ext in compressor.supported_formats):
                    input_files.append(os.path.join(root, file))
            if not args.recursive:
                break
    
    if not input_files:
        print("No image files found!")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    print(f"Found {len(input_files)} image(s) to compress")
    print(f"Using method: {args.method}")
    print(f"Quality: {args.quality}")
    print(f"Max dimensions: {args.max_width}x{args.max_height}")
    print()
    
    successful = 0
    failed = 0
    total_original_size = 0
    total_compressed_size = 0
    
    for i, input_path in enumerate(input_files):
        try:
            print(f"Processing {i+1}/{len(input_files)}: {os.path.basename(input_path)}")
            
            # Generate output filename
            filename = os.path.basename(input_path)
            name, ext = os.path.splitext(filename)
            
            # Determine output format
            if args.method == "WebP Conversion":
                output_ext = ".webp"
            elif args.method == "PNG Optimization":
                output_ext = ".png"
            else:
                output_ext = ".jpg"
            
            output_filename = f"{name}_compressed{output_ext}"
            output_path = os.path.join(args.output, output_filename)
            
            # Compress image
            result = compressor.compress_image(
                input_path,
                output_path,
                args.method,
                args.quality,
                (args.max_width, args.max_height)
            )
            
            if result['success']:
                successful += 1
                total_original_size += result['original_size']
                total_compressed_size += result['compressed_size']
                
                print(f"  ✓ Compressed: {format_size(result['compressed_size'])} "
                      f"({result['compression_ratio']:.1f}% reduction)")
            else:
                failed += 1
                print(f"  ✗ Error: {result['error']}")
                
        except Exception as e:
            failed += 1
            print(f"  ✗ Error: {str(e)}")
    
    # Final results
    print(f"\n=== COMPRESSION COMPLETE ===")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total original size: {format_size(total_original_size)}")
    print(f"Total compressed size: {format_size(total_compressed_size)}")
    
    if total_original_size > 0:
        total_compression_ratio = (1 - total_compressed_size / total_original_size) * 100
        print(f"Overall compression: {total_compression_ratio:.1f}%")

def format_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

if __name__ == "__main__":
    main()
