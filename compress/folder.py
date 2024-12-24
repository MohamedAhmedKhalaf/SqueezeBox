from flask import Blueprint, render_template, request, send_file, flash
import os
import shutil
import zipfile
from forms import FolderForm
from config import UPLOAD_FOLDER  # Ensure this is set in your config file

folder_bp = Blueprint('folder', __name__, url_prefix='/folder')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower()

def zip_folder(folder_path, zip_path):
    # Zips the folder at folder_path to zip_path, including all subdirectories and files
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)  # Store the file with the relative path
                zipf.write(file_path, arcname=arcname)

def sanitize_filename(filename):
    # Replace spaces and special characters with underscores
    return "".join(c if c.isalnum() or c in ['.', '_', '-', ' '] else "_" for c in filename)

@folder_bp.route('/', methods=['GET', 'POST'])
def folder():
    form = FolderForm()
    if form.validate_on_submit():
        if 'folder_file' not in request.files:
            flash('No file part', 'error')
            return render_template('folder.html', form=form)

        files = request.files.getlist('folder_file')  # Get all files uploaded from the folder

        if not files:
            flash('No files selected', 'error')
            return render_template('folder.html', form=form)

        # Temporary folder to hold the uploaded files
        upload_dir = os.path.join(UPLOAD_FOLDER, "temp_folder")
        os.makedirs(upload_dir, exist_ok=True)

        file_name = files[0].filename
        sanitized_filename = sanitize_filename(file_name)
        zip_file_name = f"{sanitized_filename}_compressed.zip"

        # Iterate through each file and save it
        for file in files:
            if file and allowed_file(file.filename):
                # Maintain folder structure if needed
                file_path = os.path.join(upload_dir, file.filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create directories as needed
                file.save(file_path)

        zip_path = os.path.abspath(f"static/{zip_file_name}")

        # Zip the folder and its contents
        zip_folder(upload_dir, zip_path)
        shutil.rmtree(upload_dir)  # Clean up the uploaded folder

        # Check if zip file was created
        if os.path.exists(zip_path):
            return send_file(zip_path, as_attachment=True, download_name=zip_file_name)
        else:
            flash("Zip file was not created", 'error')
            return render_template('folder.html', form=form)

    return render_template('folder.html', form=form)
