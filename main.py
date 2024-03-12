import piexif
from PIL import Image
from random import uniform
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
    # Load the image
    img = Image.open(input_path)
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # Generate randomized GPS data
    lat, lon = random_gps_coord()
    gps_exif = get_exif_ifd(lat, lon)

    # Generate other randomized EXIF data
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make: input("Camera Make: "),
            piexif.ImageIFD.Model: input("Camera Model: "),
            piexif.ImageIFD.Software: input("Software: ")
        },
        "Exif": {},
        "GPS": gps_exif
    }
    exif_bytes = piexif.dump(exif_dict)

    img.save(output_path, "jpeg", exif=exif_bytes)
    print(f"Image saved with randomized EXIF data at {output_path}")


input_image_path = "job.png"
output_image_path = "/Users/Jonathan/Desktop/exif scrambler/new.png"

scramble_exif(input_image_path, output_image_path)
