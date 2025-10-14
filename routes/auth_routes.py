from flask import Blueprint, render_template, request, redirect, url_for

auth_bp = Blueprint("auth", __name__)

users = {
    "student": {"username": "student", "password": "123"},
    "faculty": {"username": "faculty", "password": "123"}
}

@auth_bp.route("/")
def login_page():
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    if username == users[role]["username"] and password == users[role]["password"]:
        if role == "faculty":
            return redirect(url_for("faculty.faculty_dashboard"))
        else:
            return redirect(url_for("student.student_dashboard"))
    else:
        return "<h3>❌ Invalid credentials! <a href='/'>Try again</a></h3>"
