"""
Demo script for Image Compressor
"""

import os
import sys
from PIL import Image, ImageDraw
import numpy as np

def create_sample_images():
    """Create sample images for demonstration"""
    print("Creating sample images...")
    
    # Create assets directory if it doesn't exist
    os.makedirs("assets", exist_ok=True)
    
    # Create a colorful test image
    img1 = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img1)
    
    # Draw some shapes
    draw.rectangle([50, 50, 200, 200], fill='red', outline='black', width=3)
    draw.ellipse([300, 100, 500, 300], fill='blue', outline='black', width=3)
    draw.polygon([(600, 150), (700, 50), (750, 200), (650, 250)], fill='green', outline='black', width=3)
    
    # Add some text
    try:
        draw.text((100, 400), "Sample Image for Compression", fill='black')
    except:
        pass  # Skip text if font not available
    
    img1.save("assets/sample_image.jpg", "JPEG", quality=95)
    print("✓ Created sample_image.jpg")
    
    # Create a gradient image
    img2 = Image.new('RGB', (400, 400))
    pixels = np.array(img2)
    
    for i in range(400):
        for j in range(400):
            pixels[i, j] = [i//2, j//2, (i+j)//4]
    
    img2 = Image.fromarray(pixels.astype('uint8'))
    img2.save("assets/gradient_image.png", "PNG")
    print("✓ Created gradient_image.png")
    
    # Create a simple pattern
    img3 = Image.new('RGB', (300, 300), color='white')
    draw = ImageDraw.Draw(img3)
    
    for i in range(0, 300, 20):
        for j in range(0, 300, 20):
            if (i//20 + j//20) % 2 == 0:
                draw.rectangle([i, j, i+20, j+20], fill='black')
    
    img3.save("assets/pattern_image.bmp", "BMP")
    print("✓ Created pattern_image.bmp")

def run_demo():
    """Run a demonstration of the compressor"""
    print("=== Image Compressor Demo ===\n")
    
    # Create sample images
    create_sample_images()
    
    # Import the compressor
    try:
        from src.image_compressor import ImageCompressor
        compressor = ImageCompressor()
        
        print("\nTesting compression methods...")
        
        # Test different compression methods
        methods = ['JPEG Quality', 'PNG Optimization', 'WebP Conversion', 'Size Reduction']
        
        for method in methods:
            print(f"\nTesting {method}:")
            
            input_path = "assets/sample_image.jpg"
            output_path = f"assets/compressed_{method.lower().replace(' ', '_')}"
            
            # Determine output extension
            if method == "WebP Conversion":
                output_path += ".webp"
            elif method == "PNG Optimization":
                output_path += ".png"
            else:
                output_path += ".jpg"
            
            result = compressor.compress_image(
                input_path,
                output_path,
                method,
                quality=80,
                max_size=(400, 300)
            )
            
            if result['success']:
                print(f"  ✓ Success! Compression ratio: {result['compression_ratio']:.1f}%")
                print(f"  Original: {result['original_size']} bytes")
                print(f"  Compressed: {result['compressed_size']} bytes")
            else:
                print(f"  ✗ Failed: {result['error']}")
        
        print("\n=== Demo Complete ===")
        print("Check the 'assets' folder for original and compressed images!")
        print("\nTo run the GUI application:")
        print("python src/image_compressor.py")
        print("\nTo run the CLI:")
        print("python src/cli_compressor.py assets/sample_image.jpg -o compressed/ -q 80")
        
    except ImportError as e:
        print(f"Error importing compressor: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    run_demo()
