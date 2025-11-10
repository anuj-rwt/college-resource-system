from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for, flash, session, current_app, abort
import os
from werkzeug.utils import secure_filename
from models import db, File

faculty_bp = Blueprint("faculty", __name__, url_prefix="")

ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(fn):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login_page"))
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def faculty_only(fn):
    def wrapper(*args, **kwargs):
        if session.get("role") != "faculty":
            return abort(403, description="Only faculty can access this page")
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@faculty_bp.route("/faculty")
@login_required
@faculty_only
def faculty_dashboard():
    return render_template("faculty.html")

@faculty_bp.route('/upload', methods=['POST'])
@login_required
@faculty_only
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")

        base, ext = os.path.splitext(filename)
        counter = 1
        final_filename = filename
        while os.path.exists(os.path.join(upload_folder, final_filename)):
            final_filename = f"{base}_{counter}{ext}"
            counter += 1

        save_path = os.path.join(upload_folder, final_filename)
        file.save(save_path)

        # form data
        user_id = session.get('user_id')
        resource_type = request.form.get('resource_type')
        course = request.form.get('course')
        year = request.form.get('year')
        semester = request.form.get('semester')
        exam_type = request.form.get('exam_type')

        new_file = File(
            filename=final_filename,
            filepath=save_path,
            uploaded_by=user_id,
            resource_type=resource_type,
            course=course,
            year=year,
            semester=semester,
            exam_type=exam_type
        )
        db.session.add(new_file)
        db.session.commit()

        flash('File uploaded successfully!')
        return redirect(url_for('faculty.faculty_dashboard'))
    else:
        flash('Invalid file type. Only PDF allowed.')
        return redirect(request.url)

@faculty_bp.route("/uploads/<filename>")
def serve_file(filename):
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    return send_from_directory(upload_folder, filename)
