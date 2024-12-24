from flask import Blueprint, render_template, request, send_file, flash
import os
import shutil
import zipfile
from forms import FolderForm
from config import UPLOAD_FOLDER  #removed output folder

folder_bp = Blueprint('folder', __name__, url_prefix='/folder')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower()

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname=arcname)

def sanitize_filename(filename):
    # Replace spaces and special characters with underscores
    filename = "".join(c if c.isalnum() or c in ['.', '_'] else "_" for c in filename)
    return filename

@folder_bp.route('/', methods=['GET', 'POST'])
def folder():
    form = FolderForm()
    if form.validate_on_submit():
        if 'folder_file' not in request.files:
            flash('No file part', 'error')
            return render_template('folder.html', form=form)
        file = form.folder_file.data
        if file.filename == '':
            flash('No selected file', 'error')
            return render_template('folder.html', form=form)

        if file:
            sanitized_filename = sanitize_filename(file.filename)
            upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(upload_path)
            zip_file_name = f'{sanitized_filename}.zip'
            output_folder = "static" # Hardcoded output folder
            # Handle if the uploaded item is a folder
            if os.path.isdir(upload_path):
                zip_path = os.path.abspath(f"{output_folder}/{zip_file_name}")
                print("Zip Folder Path:", zip_path)
                zip_folder(upload_path, zip_path)
                shutil.rmtree(upload_path)  # Clean up the uploaded folder
                 # check if the file exists
                if os.path.exists(zip_path):
                     return send_file(zip_path, as_attachment=True, download_name=zip_file_name)
                else:
                    flash("Zip file was not created","error")
                    return render_template('folder.html', form=form)


            # Handle if the uploaded item is a file
            else:
                zip_path = os.path.abspath(f"{output_folder}/{zip_file_name}")
                print("Zip File Path:", zip_path)
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(upload_path, arcname=sanitized_filename)
                os.remove(upload_path)  # Clean up the uploaded file
                # check if the file exists
                if os.path.exists(zip_path):
                     return send_file(zip_path, as_attachment=True, download_name=zip_file_name)
                else:
                    flash("Zip file was not created","error")
                    return render_template('folder.html', form=form)


    return render_template('folder.html', form=form)