from datetime import datetime
from flask import Blueprint, render_template, session, redirect, url_for
from models import File

student_bp = Blueprint("student", __name__, url_prefix="")

def login_required(fn):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login_page"))
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@student_bp.route("/student")
@login_required
def student_dashboard():
    resource_types = ["PYQ", "Notes", "Assignments"]
    return render_template("student.html", level="resource", options=resource_types, path=[])

@student_bp.route("/student/<resource_type>")
@login_required
def select_course(resource_type):
    files = File.query.filter_by(resource_type=resource_type).all()
    courses = sorted(list({f.course for f in files}))
    return render_template("student.html", level="course", options=courses, path=[resource_type])

@student_bp.route("/student/<resource_type>/<course>")
@login_required
def select_year(resource_type, course):
    files = File.query.filter_by(resource_type=resource_type, course=course).all()
    years = sorted(list({f.year for f in files}))
    return render_template("student.html", level="year", options=years, path=[resource_type, course])

@student_bp.route("/student/<resource_type>/<course>/<year>")
@login_required
def select_semester(resource_type, course, year):
    files = File.query.filter_by(resource_type=resource_type, course=course, year=year).all()
    semesters = sorted(list({f.semester for f in files}))
    return render_template("student.html", level="semester", options=semesters, path=[resource_type, course, year])

@student_bp.route("/student/<resource_type>/<course>/<year>/<semester>")
@login_required
def select_exam(resource_type, course, year, semester):
    files = File.query.filter_by(resource_type=resource_type, course=course, year=year, semester=semester).all()
    exams = sorted(list({f.exam_type for f in files}))
    return render_template("student.html", level="exam", options=exams, path=[resource_type, course, year, semester])

@student_bp.route("/student/<resource_type>/<course>/<year>/<semester>/<exam_type>")
@login_required
def show_files(resource_type, course, year, semester, exam_type):
    files = File.query.filter_by(
        resource_type=resource_type,
        course=course,
        year=year,
        semester=semester,
        exam_type=exam_type
    ).order_by(File.upload_time.desc()).all()

    for f in files:
        if isinstance(f.upload_time, str):
            try:
                f.upload_time = datetime.fromisoformat(f.upload_time)
            except ValueError:
                pass 

    return render_template(
        "student.html",
        level="files",
        files=files,
        path=[resource_type, course, year, semester, exam_type]
    )
