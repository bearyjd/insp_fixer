import os
import shutil
import argparse
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image
from tqdm import tqdm

class StereoscopicValidator:
    def __init__(self):
        self.valid_dimensions = [
            (4000, 2000),
            (3840, 1920),
        ]
    
    def validate_image(self, image_path: str) -> Tuple[bool, str]:
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                
                if (width, height) in self.valid_dimensions:
                    return True, f"Valid stereoscopic dimensions: {width}x{height}"
                
                if abs(width/height - 2.0) < 0.1:
                    return True, f"Appears to be stereoscopic: {width}x{height}"
                
                return False, f"Invalid dimensions for stereoscopic image: {width}x{height}"
                
        except Exception as e:
            return False, f"Error validating image: {str(e)}"

class InspAnalyzer:
    JPEG_START_MARKER = bytes([0xFF, 0xD8])
    JPEG_END_MARKER = bytes([0xFF, 0xD9])
    
    def __init__(self, insp_path: str):
        self.insp_path = insp_path
        self.header_size = 0
        self.footer_size = 0
        self.total_size = 0
        self.image_size = 0
        self.analyze_file()
    
    def find_jpeg_boundaries(self, data: bytes) -> Tuple[int, int]:
        start_pos = data.find(self.JPEG_START_MARKER)
        if start_pos == -1:
            raise ValueError("No JPEG start marker found in INSP file")
        
        end_pos = data.rfind(self.JPEG_END_MARKER)
        if end_pos == -1:
            raise ValueError("No JPEG end marker found in INSP file")
        
        return start_pos, end_pos + 2
    
    def analyze_file(self):
        with open(self.insp_path, 'rb') as f:
            data = f.read()
            self.total_size = len(data)
            
            jpeg_start, jpeg_end = self.find_jpeg_boundaries(data)
            
            self.header_size = jpeg_start
            self.image_size = jpeg_end - jpeg_start
            self.footer_size = self.total_size - jpeg_end
            
            self.version_info = self.extract_version_info(data[:self.header_size])
    
    def extract_version_info(self, header_data: bytes) -> Optional[str]:
        try:
            version_marker = b"v1.5.3"
            pos = header_data.find(version_marker)
            if pos != -1:
                return version_marker.decode('ascii')
        except Exception:
            pass
        return None

def create_insp_from_jpg(jpg_path: str, template_insp_path: str, output_path: str, analyzer: InspAnalyzer):
    with open(template_insp_path, 'rb') as f:
        template_data = f.read()
    
    with open(output_path, 'wb') as outfile:
        outfile.write(template_data[:analyzer.header_size])
        
        with open(jpg_path, 'rb') as jpg_file:
            jpg_data = jpg_file.read()
            outfile.write(jpg_data)
        
        if analyzer.footer_size > 0:
            footer_start = analyzer.header_size + analyzer.image_size
            footer_data = template_data[footer_start:footer_start + analyzer.footer_size]
            outfile.write(footer_data)

def process_single_file(jpg_path: str, output_dir: str, template_insp_path: str, verbose: bool = False):
    """Process a single JPG file"""
    jpg_path = Path(jpg_path)
    output_path = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize validator
    validator = StereoscopicValidator()
    
    try:
        # Analyze template INSP file
        analyzer = InspAnalyzer(template_insp_path)
        if verbose:
            print(f"\nTemplate INSP analysis:")
            print(f"  Header size: {analyzer.header_size} bytes")
            print(f"  Footer size: {analyzer.footer_size} bytes")
            print(f"  Total size: {analyzer.total_size} bytes")
            if analyzer.version_info:
                print(f"  Version detected: {analyzer.version_info}\n")
        
        # Validate image
        is_valid, validation_msg = validator.validate_image(str(jpg_path))
        if verbose:
            print(f"Validating {jpg_path.name}: {validation_msg}")
        
        if not is_valid:
            print(f"Skipping {jpg_path.name}: {validation_msg}")
            return
        
        # Create output paths
        insp_file = output_path / f"{jpg_path.stem}.insp"
        jpg_output = output_path / jpg_path.name
        
        # Convert file
        create_insp_from_jpg(jpg_path, template_insp_path, insp_file, analyzer)
        
        # Copy original JPG
        if jpg_path != jpg_output:
            shutil.copy2(jpg_path, jpg_output)
        
        if verbose:
            print(f"Successfully processed {jpg_path.name}")
            print(f"Created: {insp_file}")
            
    except Exception as e:
        print(f"Error processing {jpg_path.name}: {str(e)}")

def process_directory(input_dir: str, output_dir: str, template_insp_path: str, verbose: bool = False):
    """Process all JPG files in a directory"""
    input_path = Path(input_dir)
    jpg_files = list(input_path.glob('*.jpg'))
    
    with tqdm(total=len(jpg_files), desc="Processing files", unit="file") as pbar:
        for jpg_file in jpg_files:
            process_single_file(jpg_file, output_dir, template_insp_path, verbose)
            pbar.update(1)

def main():
    parser = argparse.ArgumentParser(description='Convert stereoscopic JPGs to INSP format')
    parser.add_argument('input', help='Input JPG file or directory containing JPG files')
    parser.add_argument('output_dir', help='Directory to save converted INSP files')
    parser.add_argument('template_insp', help='Path to reference INSP file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Check if input is a file or directory
    input_path = Path(args.input)
    if input_path.is_file():
        process_single_file(args.input, args.output_dir, args.template_insp, args.verbose)
    elif input_path.is_dir():
        process_directory(args.input, args.output_dir, args.template_insp, args.verbose)
    else:
        print(f"Error: {args.input} is not a valid file or directory")

if __name__ == "__main__":
    main()
