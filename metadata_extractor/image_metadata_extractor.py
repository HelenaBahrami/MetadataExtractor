import argparse
import json
import os
from datetime import datetime
from typing import Dict

from PIL import Image
from PIL.ExifTags import TAGS


class MetadataExtractor:
    def __init__(self, input_path: str, output_dir: str):
        self.input_path = input_path
        self.output_dir = output_dir

    def extract_metadata(self):
        try:
            image = Image.open(self.input_path)
            filesystem_metadata = self.extract_filesystem_metadata()
            exif_data = image.getexif()
            image_metadata = self.extract_image_metadata(exif_data)
            metadata = {**filesystem_metadata, **image_metadata}

            output_path = os.path.join(self.output_dir, self.get_output_filename())
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=4)

            print(f"Metadata written to {output_path}")
        except Exception as e:
            print(f"Error processing {self.input_path}: {e}")

    def extract_filesystem_metadata(self) -> Dict:
        stat_info = os.stat(self.input_path)
        return {
            "filename": os.path.basename(self.input_path),
            "size": stat_info.st_size,
            "created_time": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
            "modified_time": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
        }

    def extract_image_metadata(self, exif_data) -> Dict:
        metadata = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "DateTimeOriginal":
                metadata["capture_time"] = datetime.strptime(value, "%Y:%m:%d  %H:%M:%S").isoformat()
            elif tag == "Model":
                metadata["camera_model"] = value
            elif tag == "BodySerialNumber":
                metadata["camera_serial"] = value
            elif tag == "Orientation":
                metadata["orientation"] = value
        return metadata

    def get_output_filename(self) -> str:
        filename, extension = os.path.splitext(os.path.basename(self.input_path))
        return f"{filename}.json"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract metadata from JPEG images')
    parser.add_argument('-i', '--input', nargs='+', required=True, help='Input JPEG file(s)')
    parser.add_argument('-o', '--output-dir', required=True, help='Output directory for metadata files')
    args = parser.parse_args()

    for input_path in args.input:
        extractor = MetadataExtractor(input_path, args.output_dir)
        extractor.extract_metadata()
