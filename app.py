from flask import Flask, render_template, request, redirect, send_from_directory, jsonify, url_for
import os, datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# === DSA: Linked List for Uploaded Files ===
class FileNode:
    def __init__(self, filename, resource_type, course, year, semester, exam_type, filepath):
        self.filename = filename
        self.resource_type = resource_type
        self.course = course
        self.year = year
        self.semester = semester
        self.exam_type = exam_type
        self.filepath = filepath
        self.upload_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.next = None

class FileLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, filename, resource_type, course, year, semester, exam_type, filepath):
        """Insert new file node at the end"""
        new_node = FileNode(filename, resource_type, course, year, semester, exam_type, filepath)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def filter_files(self, **kwargs):
        """Filter files based on hierarchy"""
        results = []
        temp = self.head
        while temp:
            match = True
            for key, value in kwargs.items():
                if getattr(temp, key) != value:
                    match = False
                    break
            if match:
                results.append(temp)
            temp = temp.next
        return results

# Linked list object
uploaded_files = FileLinkedList()

# Users
users = {
    "student": {"username": "student", "password": "123"},
    "faculty": {"username": "faculty", "password": "123"}
}

# === ROUTES ===

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    if username == users[role]["username"] and password == users[role]["password"]:
        if role == "faculty":
            return redirect(url_for("faculty_dashboard"))
        else:
            return redirect(url_for("student_dashboard"))
    else:
        return "<h3>❌ Invalid credentials! <a href='/'>Try again</a></h3>"

# === Faculty ===
@app.route("/faculty")
def faculty_dashboard():
    return render_template("faculty.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["pdfFile"]
    if not file:
        return "No file uploaded!"

    filename = file.filename
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Get hierarchy info
    resource_type = request.form["resource_type"]
    course = request.form["course"]
    year = request.form["year"]
    semester = request.form["semester"]
    exam_type = request.form["exam_type"]

    uploaded_files.insert(filename, resource_type, course, year, semester, exam_type, f"/uploads/{filename}")

    return "<h3>✅ File uploaded successfully! <a href='/faculty'>Go back</a></h3>"

# Serve uploaded PDFs
@app.route("/uploads/<filename>")
def serve_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# === Student ===
@app.route("/student")
def student_dashboard():
    # Show resource types: PYQ, Notes, Assignments
    resource_types = ["PYQ", "Notes", "Assignments"]
    return render_template("student.html", level="resource", options=resource_types, path=[])

@app.route("/student/<resource_type>")
def select_course(resource_type):
    # Show unique courses for this resource_type
    courses = list(set([f.course for f in uploaded_files.filter_files(resource_type=resource_type)]))
    return render_template("student.html", level="course", options=courses, path=[resource_type])

@app.route("/student/<resource_type>/<course>")
def select_year(resource_type, course):
    years = list(set([f.year for f in uploaded_files.filter_files(resource_type=resource_type, course=course)]))
    return render_template("student.html", level="year", options=years, path=[resource_type, course])

@app.route("/student/<resource_type>/<course>/<year>")
def select_semester(resource_type, course, year):
    semesters = list(set([f.semester for f in uploaded_files.filter_files(resource_type=resource_type, course=course, year=year)]))
    return render_template("student.html", level="semester", options=semesters, path=[resource_type, course, year])

@app.route("/student/<resource_type>/<course>/<year>/<semester>")
def select_exam(resource_type, course, year, semester):
    exams = list(set([f.exam_type for f in uploaded_files.filter_files(resource_type=resource_type, course=course, year=year, semester=semester)]))
    return render_template("student.html", level="exam", options=exams, path=[resource_type, course, year, semester])

@app.route("/student/<resource_type>/<course>/<year>/<semester>/<exam_type>")
def show_files(resource_type, course, year, semester, exam_type):
    files = uploaded_files.filter_files(
        resource_type=resource_type,
        course=course,
        year=year,
        semester=semester,
        exam_type=exam_type
    )
    return render_template("student.html", level="files", files=files, path=[resource_type, course, year, semester, exam_type])

if __name__ == "__main__":
    app.run(debug=True)

