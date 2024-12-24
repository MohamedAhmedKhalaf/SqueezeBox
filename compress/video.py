import os
from flask import Blueprint, render_template, flash, current_app
from werkzeug.utils import secure_filename
import subprocess
from forms import VideoForm
from config import OUTPUT_FOLDER

video_bp = Blueprint('video', __name__)

def compress_video_ffmpeg(input_path, output_path, target_size_mb):
    try:
        target_bitrate = (target_size_mb * 8 * 1024 * 1024) / os.path.getsize(input_path)
        
        command = [
            "ffmpeg",
            "-i", input_path,
            "-vcodec", "libx264",
            "-crf", "28",
            "-b:v", f"{int(target_bitrate)}k",
            "-preset", "medium",
            output_path,
        ]
        subprocess.run(command, check=True)
        return None
    except Exception as e:
        return str(e)

@video_bp.route('/video', methods=['GET', 'POST'])
def video():
    form = VideoForm()
    
    if form.validate_on_submit():
        if form.video_file.data:
            try:
                os.makedirs(OUTPUT_FOLDER, exist_ok=True)
                
                filename = secure_filename(form.video_file.data.filename)
                input_path = os.path.join(OUTPUT_FOLDER, f"temp_{filename}")
                output_path = os.path.join(OUTPUT_FOLDER, f"compressed_{filename}")
                
                form.video_file.data.save(input_path)
                target_size_mb = max(0.5, form.target_size_mb.data)
                
                error = compress_video_ffmpeg(input_path, output_path, target_size_mb)
                
                if error:
                    flash(f"Compression error: {error}", 'danger')
                else:
                    flash(f"Video compressed successfully! File saved as: compressed_{filename}", 'success')
                
            except Exception as e:
                flash(f"Error: {str(e)}", 'danger')
                
            finally:
                if os.path.exists(input_path):
                    os.remove(input_path)
    
    return render_template('video.html', form=form)