import os
from dotenv import load_dotenv

load_dotenv()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'jpg', 'jpeg', 'png', 'mp4', 'mov', 'mp3', 'wav', 'mkv', 'avi'}
OUTPUT_FOLDER = 'static/'
UPLOAD_FOLDER = 'uploads/' # Add this line