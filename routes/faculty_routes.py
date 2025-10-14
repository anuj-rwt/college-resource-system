from flask import Blueprint, render_template, request, send_from_directory
import os

faculty_bp = Blueprint("faculty", __name__)
uploaded_files = None  # will be injected later
UPLOAD_FOLDER = "uploads"

@faculty_bp.route("/faculty")
def faculty_dashboard():
    return render_template("faculty.html")

@faculty_bp.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["pdfFile"]
    if not file:
        return "No file uploaded!"

    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    resource_type = request.form["resource_type"]
    course = request.form["course"]
    year = request.form["year"]
    semester = request.form["semester"]
    exam_type = request.form["exam_type"]

    uploaded_files.insert(filename, resource_type, course, year, semester, exam_type, f"/uploads/{filename}")

    return "<h3>✅ File uploaded successfully! <a href='/faculty'>Go back</a></h3>"

@faculty_bp.route("/uploads/<filename>")
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
