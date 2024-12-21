import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here')
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'jpg', 'jpeg', 'png', 'mp4', 'mov', 'mp3', 'wav'}
OUTPUT_FOLDER = 'static/uploads/output' 