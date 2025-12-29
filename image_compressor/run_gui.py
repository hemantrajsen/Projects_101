#!/usr/bin/env python3
"""
Launcher script for Image Compressor GUI
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from image_compressor import main
    main()
except ImportError as e:
    print(f"Error importing image compressor: {e}")
    print("Make sure all dependencies are installed:")
    print("pip3 install -r requirements.txt")
    sys.exit(1)
