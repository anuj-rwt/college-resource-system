from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint("auth", __name__)

def ensure_default_users():
    defaults = [
        {"username": "admin", "email": "admin@crms.com", "password": "admin123", "role": "admin"},
        {"username": "faculty", "email": "faculty@crms.com", "password": "faculty123", "role": "faculty"},
        {"username": "student", "email": "student@crms.com", "password": "student123", "role": "student"}
    ]

    for u in defaults:
        existing = User.query.filter_by(username=u["username"]).first()
        if not existing:
            new_user = User(
                username=u["username"],
                email=u["email"],
                password_hash=generate_password_hash(u["password"]),
                role=u["role"]
            )
            db.session.add(new_user)
    db.session.commit()

@auth_bp.before_app_request
def _init_defaults():
    try:
        ensure_default_users()
    except Exception:
        pass

@auth_bp.route("/")
def login_page():
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role")
    if not all([username, password, role]):
        flash("Please fill all fields.")
        return redirect(url_for("auth.login_page"))

    user = User.query.filter_by(username=username, role=role).first()
    if user and check_password_hash(user.password_hash, password):
        session.clear()
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role
        if role == "faculty":
            return redirect(url_for("faculty.faculty_dashboard"))
        else:
            return redirect(url_for("student.student_dashboard"))
    else:
        flash("Invalid credentials.")
        return redirect(url_for("auth.login_page"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login_page"))

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role")
    if not all([username, email, password, role]):
        flash("Please fill all fields.")
        return redirect(url_for("auth.signup"))
    if User.query.filter_by(username=username).first():
        flash("Username already exists.")
        return redirect(url_for("auth.signup"))
    new_user = User(username=username, email=email, role=role, password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    flash("Registration successful. Please login.")
    return redirect(url_for("auth.login_page"))
