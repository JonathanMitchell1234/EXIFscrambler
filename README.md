# EXIFscrambler

A Python script that poisons an image's EXIF data with randomized information.

This Python script scrambles the EXIF metadata of images, including GPS coordinates and camera make/model. It's useful for adding a layer of privacy to your photos before sharing them online. Many websites/apps say that they strip this data and delete it, but do you trust them to do so?

## How it works

The script works by loading an image, generating random EXIF metadata, and then saving the image with the new metadata. The EXIF metadata includes GPS coordinates, camera make, and camera model.

## Usage

1. Specify the input and output directories at the bottom of the script:

```python
input_directory = "/path/to/your/input/directory"
output_directory = "/path/to/your/output/directory"
```

2. Run the script:

```bash
python main.py
```

The script will process all images in the input directory and save the scrambled images to the output directory.

## Functions

- `convert_to_rational(number)`: Converts a number to a rational tuple (numerator, denominator).
- `get_exif_ifd(lat, lon)`: Generates EXIF data for GPS coordinates.
- `random_gps_coord()`: Generates random GPS coordinates.
- `scramble_exif(input_path, output_path)`: Loads an image, generates random EXIF metadata, and saves the image with the new metadata.
- `process_batch(input_dir, output_dir)`: Processes all images in the input directory and saves the scrambled images to the output directory.

## Dependencies

- Python 3
- [piexif](https://pypi.org/project/piexif/)
- [Pillow](https://pypi.org/project/Pillow/)

## Installation

1. Install Python 3: https://www.python.org/downloads/
2. Install the dependencies:

```bash
pip install piexif Pillow
```

3. Download the script and run it as described in the Usage section.