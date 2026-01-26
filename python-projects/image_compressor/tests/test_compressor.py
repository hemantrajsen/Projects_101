"""
Test suite for Image Compressor
"""

import unittest
import os
import tempfile
from PIL import Image
import numpy as np
from src.image_compressor import ImageCompressor

class TestImageCompressor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.compressor = ImageCompressor()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a test image
        self.test_image_path = os.path.join(self.temp_dir, "test.jpg")
        self.create_test_image()
    
    def create_test_image(self):
        """Create a test image for compression tests"""
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img.save(self.test_image_path, 'JPEG', quality=95)
    
    def test_compression_methods(self):
        """Test all compression methods"""
        methods = self.compressor.compression_methods.keys()
        
        for method in methods:
            with self.subTest(method=method):
                output_path = os.path.join(self.temp_dir, f"test_{method.lower().replace(' ', '_')}.jpg")
                
                result = self.compressor.compress_image(
                    self.test_image_path,
                    output_path,
                    method,
                    quality=80
                )
                
                self.assertTrue(result['success'], f"Method {method} failed")
                self.assertGreater(result['compression_ratio'], 0)
                self.assertTrue(os.path.exists(output_path))
    
    def test_quality_settings(self):
        """Test different quality settings"""
        qualities = [50, 70, 85, 95]
        
        for quality in qualities:
            with self.subTest(quality=quality):
                output_path = os.path.join(self.temp_dir, f"test_q{quality}.jpg")
                
                result = self.compressor.compress_image(
                    self.test_image_path,
                    output_path,
                    'JPEG Quality',
                    quality=quality
                )
                
                self.assertTrue(result['success'])
                self.assertTrue(os.path.exists(output_path))
    
    def test_size_reduction(self):
        """Test size reduction functionality"""
        max_size = (50, 50)
        output_path = os.path.join(self.temp_dir, "test_resized.jpg")
        
        result = self.compressor.compress_image(
            self.test_image_path,
            output_path,
            'Size Reduction',
            quality=85,
            max_size=max_size
        )
        
        self.assertTrue(result['success'])
        
        # Check if image was actually resized
        with Image.open(output_path) as img:
            self.assertLessEqual(img.width, max_size[0])
            self.assertLessEqual(img.height, max_size[1])
    
    def test_unsupported_format(self):
        """Test handling of unsupported formats"""
        # Create a text file with .jpg extension
        fake_image_path = os.path.join(self.temp_dir, "fake.jpg")
        with open(fake_image_path, 'w') as f:
            f.write("This is not an image")
        
        output_path = os.path.join(self.temp_dir, "output.jpg")
        
        result = self.compressor.compress_image(
            fake_image_path,
            output_path,
            'JPEG Quality',
            quality=85
        )
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()
