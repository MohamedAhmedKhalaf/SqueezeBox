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
    video_file = FileField("Select Video", validators=[FileAllowed(ALLOWED_EXTENSIONS), DataRequired()])
    target_size = StringField("Target Size (MB)", default="10", validators=[DataRequired()])
    use_gpu = SelectField("Use GPU", choices=[("True", "Yes"), ("False", "No")])
    output_location = StringField("Output Location", default="compressed", validators=[DataRequired()])
    submit = SubmitField("Compress Video")


class AudioForm(FlaskForm):
    pass