from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, StringField, IntegerField, SelectField
from wtforms.validators import DataRequired
from config import ALLOWED_EXTENSIONS

class TextForm(FlaskForm):
    text_data = StringField("Enter Text:")
    submit = SubmitField("Compress Text")

class ImageForm(FlaskForm):
    image_file = FileField("Select Image", validators=[FileAllowed(ALLOWED_EXTENSIONS)])
    compression_level = SelectField("Compression Level", choices=[("high", "High"), ("medium", "Medium"), ("low", "Low")])
    submit = SubmitField("Compress Image")

class VideoForm(FlaskForm):
    video_file = FileField("Select Video", validators=[FileAllowed(ALLOWED_EXTENSIONS)])
    target_size_mb = IntegerField("Target size (MB)", default=10)
    submit = SubmitField("Compress Video")

class AudioForm(FlaskForm):
    audio_file = FileField("Select Audio", validators=[FileAllowed(ALLOWED_EXTENSIONS)])
    submit = SubmitField("Compress Audio")

class FolderForm(FlaskForm):
    folder_file = FileField("Select Folder", validators=[])
    submit = SubmitField("Compress Folder")