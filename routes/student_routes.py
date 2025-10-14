from flask import Blueprint, render_template

student_bp = Blueprint("student", __name__)
uploaded_files = None  # will be injected later

@student_bp.route("/student")
def student_dashboard():
    resource_types = ["PYQ", "Notes", "Assignments"]
    return render_template("student.html", level="resource", options=resource_types, path=[])

@student_bp.route("/student/<resource_type>")
def select_course(resource_type):
    courses = list(set([f.course for f in uploaded_files.filter_files(resource_type=resource_type)]))
    return render_template("student.html", level="course", options=courses, path=[resource_type])

@student_bp.route("/student/<resource_type>/<course>")
def select_year(resource_type, course):
    years = list(set([f.year for f in uploaded_files.filter_files(resource_type=resource_type, course=course)]))
    return render_template("student.html", level="year", options=years, path=[resource_type, course])

@student_bp.route("/student/<resource_type>/<course>/<year>")
def select_semester(resource_type, course, year):
    semesters = list(set([f.semester for f in uploaded_files.filter_files(resource_type=resource_type, course=course, year=year)]))
    return render_template("student.html", level="semester", options=semesters, path=[resource_type, course, year])

@student_bp.route("/student/<resource_type>/<course>/<year>/<semester>")
def select_exam(resource_type, course, year, semester):
    exams = list(set([f.exam_type for f in uploaded_files.filter_files(resource_type=resource_type, course=course, year=year, semester=semester)]))
    return render_template("student.html", level="exam", options=exams, path=[resource_type, course, year, semester])

@student_bp.route("/student/<resource_type>/<course>/<year>/<semester>/<exam_type>")
def show_files(resource_type, course, year, semester, exam_type):
    files = uploaded_files.filter_files(
        resource_type=resource_type,
        course=course,
        year=year,
        semester=semester,
        exam_type=exam_type
    )
    return render_template("student.html", level="files", files=files, path=[resource_type, course, year, semester, exam_type])
