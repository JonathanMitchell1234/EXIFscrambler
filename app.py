from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
import piexif
from PIL import Image
from random import choice, uniform
from fractions import Fraction

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    files = request.files.getlist('file')

    for file in files:
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            if os.path.isdir(input_path):
                process_folder(input_path, app.config['PROCESSED_FOLDER'])
            else:
                file.save(input_path)
                output_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
                try:
                    scramble_exif(input_path, output_path)
                except Exception as e:
                    print(f"Error processing single file {filename}: {e}")

    return 'Files uploaded and processed successfully'

def process_folder(folder_path, output_folder):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and allowed_file(item):
            output_path = os.path.join(output_folder, item)
            try:
                scramble_exif(item_path, output_path)
            except Exception as e:
                print(f"Error processing {item_path}: {e}")

# ... (the rest of the code remains the same)

def convert_to_rational(number):
    fraction = Fraction.from_float(number).limit_denominator(1000000)
    return fraction.numerator, fraction.denominator

def get_exif_ifd(lat, lon):
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
    lat = uniform(-90.0, 90.0)
    lon = uniform(-180.0, 180.0)
    return lat, lon

def scramble_exif(input_path, output_path):
    camera_makes = ['Canon', 'Nikon', 'Sony', 'Fujifilm', 'Olympus', 'Panasonic', 'Leica', 'Pentax', 'Sigma', 'Hasselblad']
    camera_models = ['EOS 5D Mark IV', 'D850', 'Alpha 7R IV', 'X-T4', 'OM-D E-M1 Mark III', 'Lumix GH5', 'Q2', 'K-3 III', 'fp L', 'X1D II 50C']
    img = Image.open(input_path)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    lat, lon = random_gps_coord()
    gps_exif = get_exif_ifd(lat, lon)
    random_make = choice(camera_makes)
    random_model = choice(camera_models)
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

if __name__ == '__main__':
    app.run(debug=True)