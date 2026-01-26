# Advanced Image Compressor

A comprehensive image compression tool with multiple algorithms, modern GUI, and command-line interface support.

## Features

- **Multiple Compression Methods**:
  - JPEG Quality Reduction
  - PNG Optimization
  - WebP Conversion
  - Size Reduction (resizing)
  - Advanced Lossy Compression (with Gaussian blur)

- **Supported Formats**: JPEG, PNG, BMP, TIFF, WebP
- **Modern GUI**: Built with CustomTkinter for a sleek dark theme
- **Command Line Interface**: Perfect for batch processing and automation
- **Batch Processing**: Process multiple images or entire folders
- **Real-time Progress**: Visual progress bar and detailed results
- **Quality Control**: Adjustable quality settings (1-100)
- **Size Limits**: Set maximum width and height constraints

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### GUI Application

Run the graphical interface:

```bash
python src/image_compressor.py
```

**Features:**
- Drag and drop or browse to select images
- Choose compression method and quality
- Set maximum dimensions
- Select output directory
- Real-time progress tracking
- Detailed compression results

### Command Line Interface

For batch processing and automation:

```bash
python src/cli_compressor.py input.jpg -o output_folder -m "JPEG Quality" -q 85
```

**Options:**
- `input`: Input image file or directory
- `-o, --output`: Output directory (required)
- `-m, --method`: Compression method
- `-q, --quality`: Quality setting (1-100)
- `--max-width`: Maximum width
- `--max-height`: Maximum height
- `--recursive`: Process directories recursively

**Examples:**

```bash
# Compress a single image
python src/cli_compressor.py photo.jpg -o compressed/ -q 80

# Compress all images in a folder
python src/cli_compressor.py images/ -o compressed/ -m "WebP Conversion" -q 90

# Batch process with size reduction
python src/cli_compressor.py photos/ -o web_images/ -m "Size Reduction" --max-width 800 --max-height 600
```

## Compression Methods Explained

### 1. JPEG Quality
- Reduces JPEG quality setting
- Converts other formats to JPEG
- Best for: Photos, natural images

### 2. PNG Optimization
- Optimizes PNG compression
- Removes unnecessary metadata
- Best for: Graphics, images with transparency

### 3. WebP Conversion
- Converts to modern WebP format
- Excellent compression ratio
- Best for: Web images, modern browsers

### 4. Size Reduction
- Resizes images to specified dimensions
- Maintains aspect ratio
- Best for: Thumbnails, web optimization

### 5. Advanced Lossy
- Uses OpenCV for advanced processing
- Applies Gaussian blur for additional compression
- Best for: Maximum compression when quality loss is acceptable

## Project Structure

```
image_compressor/
├── src/
│   ├── __init__.py
│   ├── image_compressor.py    # Main GUI application
│   └── cli_compressor.py      # Command line interface
├── tests/                     # Test files
├── assets/                    # Sample images
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Dependencies

- **Pillow**: Image processing and manipulation
- **CustomTkinter**: Modern GUI framework
- **NumPy**: Numerical operations
- **OpenCV**: Advanced image processing
- **Matplotlib**: Image analysis and visualization

## Performance Tips

1. **For maximum compression**: Use "Advanced Lossy" with quality 60-70
2. **For web optimization**: Use "WebP Conversion" with quality 80-90
3. **For archival**: Use "PNG Optimization" with quality 95+
4. **For thumbnails**: Use "Size Reduction" with small dimensions

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed
2. **Memory issues**: Process images in smaller batches
3. **Format not supported**: Check if the image format is in the supported list

### Performance Optimization

- For large batches, use the CLI version
- Process images in smaller groups
- Use SSD storage for better I/O performance

## Contributing

Feel free to contribute by:
- Adding new compression algorithms
- Improving the GUI
- Adding support for more image formats
- Optimizing performance

## License

This project is open source and available under the MIT License.

## Future Enhancements

- [ ] Support for RAW image formats
- [ ] GPU acceleration for faster processing
- [ ] Cloud storage integration
- [ ] Advanced image analysis tools
- [ ] Plugin system for custom algorithms
