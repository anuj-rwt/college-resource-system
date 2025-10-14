from flask import Flask
import os

from models.file_linkedlist import FileLinkedList
from routes.auth_routes import auth_bp
from routes.faculty_routes import faculty_bp
from routes.student_routes import student_bp

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Linked List shared by all routes
uploaded_files = FileLinkedList()

# Inject into route modules
from routes import faculty_routes, student_routes
faculty_routes.uploaded_files = uploaded_files
student_routes.uploaded_files = uploaded_files

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(faculty_bp)
app.register_blueprint(student_bp)

if __name__ == "__main__":
    app.run(debug=True)
