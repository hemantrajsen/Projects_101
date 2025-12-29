# Quick Start Guide

## Installation

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

## Running the Application

### GUI Mode (Recommended)
```bash
python3 run_gui.py
```
or
```bash
python3 src/image_compressor.py
```

### Command Line Mode
```bash
# Compress a single image
python3 src/cli_compressor.py image.jpg -o output/ -q 80

# Compress all images in a folder
python3 src/cli_compressor.py images/ -o compressed/ -m "WebP Conversion" -q 90

# Batch process with size reduction
python3 src/cli_compressor.py photos/ -o web_images/ -m "Size Reduction" --max-width 800 --max-height 600
```

## Demo
Run the demo to see all compression methods in action:
```bash
python3 demo.py
```

## Compression Methods

- **JPEG Quality**: Best for photos, reduces quality setting
- **PNG Optimization**: Best for graphics with transparency
- **WebP Conversion**: Modern format with excellent compression
- **Size Reduction**: Resizes images to specified dimensions
- **Advanced Lossy**: Maximum compression with OpenCV processing

## Tips

- Use quality 80-90 for good balance of size vs quality
- WebP gives the best compression ratios
- Size reduction is great for thumbnails
- Advanced Lossy is for maximum compression when quality loss is acceptable

## Troubleshooting

If you get import errors, make sure all dependencies are installed:
```bash
pip3 install -r requirements.txt
```

For GUI issues on macOS, you might need to install tkinter:
```bash
brew install python-tk
```
