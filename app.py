from flask import Flask, render_template, request, redirect, url_for, send_file
from forms import TextForm, ImageForm, VideoForm, AudioForm
import os
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, OUTPUT_FOLDER
from compress import text as text_compress, image as image_compress, video as video_compress
import base64
from pathlib import Path
import shutil
import re
app = Flask(__name__)
app.config.from_pyfile('config.py')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def create_output_dir():
    if not os.path.exists(OUTPUT_FOLDER):
         os.makedirs(OUTPUT_FOLDER)
def create_upload_dir(): 
    if not os.path.exists(UPLOAD_FOLDER):
         os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(os.path.join(UPLOAD_FOLDER, "tmp")):
         os.makedirs(os.path.join(UPLOAD_FOLDER, "tmp"))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/text', methods=['GET', 'POST'])
def text():
    form = TextForm() # GO CHECK forms.py and u will understand and changed it if you need
    return render_template('text.html', form=form)


@app.route('/image', methods=['GET', 'POST'])
def image():
    form = ImageForm() # GO CHECK forms.py and u will understand and changed it if you need
    return render_template('image.html', form=form)


# Khalaf
@app.route('/video', methods=['GET', 'POST'])
def video():
    form = VideoForm()
    if form.validate_on_submit():
        if 'video_file' not in request.files:
            return render_template('video.html', form=form, error='No file found')
        file = request.files['video_file']
        if file.filename == '':
            return render_template('video.html', form=form, error='No file selected')
        if file and allowed_file(file.filename):
            create_upload_dir()
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            create_output_dir()
            output_name = re.sub(r"[^a-zA-Z0-9_.]", "_", form.output_location.data)  
            compressed_file, original_size, compressed_size, entropy = video_compress.compress_video_file(filename, form.target_size.data, form.use_gpu.data, output_name)
            os.remove(filename)
            if compressed_file:
                compressed_file_base64 = base64.b64encode(compressed_file).decode('utf-8')
                return render_template('video.html', form=form, compressed_file=compressed_file_base64, original_size=original_size, compressed_size=compressed_size, entropy=entropy)
            else:
                return render_template('video.html', form=form, error='Video compression Failed')
        else:
            return render_template('video.html', form=form, error="Invalid File type")
    return render_template('video.html', form=form)

@app.route('/audio', methods=['GET', 'POST'])
def audio():
    form = AudioForm()
    return render_template('audio.html', form=form)



@app.route('/folder', methods=['GET', 'POST'])
def folder():
    return render_template('folder.html')
    


''' host = 0.0.0.0 😂 عشانك بس يا مغربي '''
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
