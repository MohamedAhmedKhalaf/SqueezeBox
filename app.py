from flask import Flask, render_template
from compress.video import video_bp
from compress.folder import folder_bp
import os
import sys

from compress.text import text_bp
from compress.image import image_bp 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 500MB limit
app.register_blueprint(text_bp)
app.register_blueprint(video_bp)
app.register_blueprint(image_bp) 
app.register_blueprint(folder_bp)


@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/text')
# def text():
#     return render_template('text.html')

#@app.route('/image')
#def image():
#    return render_template('image.html')

@app.route('/audio')
def audio():
    return render_template('audio.html')



if __name__ == '__main__':
    app.run(debug=True)
