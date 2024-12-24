import os
from flask import Blueprint, render_template, flash, current_app
from werkzeug.utils import secure_filename
from PIL import Image
from forms import ImageForm
from config import OUTPUT_FOLDER

image_bp = Blueprint('image', __name__)

def compress_image(input_path, output_path, quality=30):
    try:
        original_size = os.path.getsize(input_path)

        with Image.open(input_path) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")

            img.save(output_path, "JPEG", optimize=True, quality=quality)

        compressed_size = os.path.getsize(output_path)
        compression_ratio = original_size / compressed_size

        return None, original_size, compressed_size, compression_ratio
    except Exception as e:
        return str(e), None, None, None

@image_bp.route('/image', methods=['GET', 'POST'])
def image():
    form = ImageForm()

    if form.validate_on_submit():
        if form.image_file.data:
            try:
                os.makedirs(OUTPUT_FOLDER, exist_ok=True)

                filename = secure_filename(form.image_file.data.filename)
                input_path = os.path.join(OUTPUT_FOLDER, f"temp_{filename}")
                output_path = os.path.join(OUTPUT_FOLDER, f"compressed_{filename}")

                form.image_file.data.save(input_path)

                compression_level = form.compression_level.data
                if compression_level == "low":
                    quality = 90
                elif compression_level == "medium":
                    quality = 60
                else:  # low
                    quality = 30

                error, original_size, compressed_size, compression_ratio = compress_image(input_path, output_path, quality)

                if error:
                    flash(f"Compression error: {error}", 'danger')
                else:
                    flash(f"Image compressed successfully! File saved as: compressed_{filename}", 'success')
                    flash(f"Original size: {original_size / 1024:.2f} KB", 'info')
                    flash(f"Compressed size: {compressed_size / 1024:.2f} KB", 'info')
                    flash(f"Compression ratio: {compression_ratio:.2f}", 'info')

            except Exception as e:
                flash(f"Error: {str(e)}", 'danger')

            finally:
                if os.path.exists(input_path):
                    os.remove(input_path)

    return render_template('image.html', form=form)
