import os
import piexif
from PIL import Image
from random import choice, uniform
from fractions import Fraction

def convert_to_rational(number):
    """Convert a number to a rational tuple (numerator, denominator)."""
    fraction = Fraction.from_float(number).limit_denominator(1000000)
    return fraction.numerator, fraction.denominator

def get_exif_ifd(lat, lon):
    """Generate EXIF data for GPS coordinates."""
    lat_ref = 'N' if lat >= 0 else 'S'
    lon_ref = 'E' if lon >= 0 else 'W'

    lat_deg = (convert_to_rational(abs(lat)), (0, 1), (0, 1))
    lon_deg = (convert_to_rational(abs(lon)), (0, 1), (0, 1))

    exif_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: lat_ref.encode('utf-8'),
        piexif.GPSIFD.GPSLatitude: lat_deg,
        piexif.GPSIFD.GPSLongitudeRef: lon_ref.encode('utf-8'),
        piexif.GPSIFD.GPSLongitude: lon_deg
    }
    return exif_ifd

def random_gps_coord():
    """Generate random GPS coordinates."""
    lat = uniform(-90.0, 90.0)
    lon = uniform(-180.0, 180.0)
    return lat, lon

def scramble_exif(input_path, output_path):
    # List of camera makes and models
    camera_makes = ['Canon', 'Nikon', 'Sony', 'Fujifilm', 'Olympus', 'Panasonic', 'Leica', 'Pentax', 'Sigma', 'Hasselblad']
    camera_models = ['EOS 5D Mark IV', 'D850', 'Alpha 7R IV', 'X-T4', 'OM-D E-M1 Mark III', 'Lumix GH5', 'Q2', 'K-3 III', 'fp L', 'X1D II 50C']

    # Load the image
    img = Image.open(input_path)
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # Generate randomized GPS data
    lat, lon = random_gps_coord()
    gps_exif = get_exif_ifd(lat, lon)

    # Select a random make and model
    random_make = choice(camera_makes)
    random_model = choice(camera_models)

    # Generate randomized EXIF data
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make: random_make,
            piexif.ImageIFD.Model: random_model,
            piexif.ImageIFD.Software: "RandomSoftware"
        },
        "Exif": {},
        "GPS": gps_exif
    }
    exif_bytes = piexif.dump(exif_dict)

    img.save(output_path, "jpeg", exif=exif_bytes)
    print(f"Image saved with randomized EXIF data at {output_path}")

def process_batch(input_dir, output_dir):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each image in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            try:
                scramble_exif(input_path, output_path)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Specify your input and output directories
input_directory = "/path/to/your/input/directory"
output_directory = "/path/to/your/output/directory"

process_batch(input_directory, output_directory)
