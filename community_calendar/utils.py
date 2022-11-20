import time
from werkzeug.utils import secure_filename
import hashlib

ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png")

def allowed_file(filename):     
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def append_timestamp_and_hash(filename: str):
    extension = filename.rsplit(".",1)[1]
    filename = secure_filename(filename) + str(time.time_ns())
    return hashlib.md5(filename.encode('utf-8')).hexdigest() + "." + extension