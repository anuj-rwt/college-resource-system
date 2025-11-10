from flask import Flask, send_from_directory
from models import db
from routes.auth_routes import auth_bp
from routes.faculty_routes import faculty_bp
from routes.student_routes import student_bp
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college_resources.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(faculty_bp)
app.register_blueprint(student_bp)

with app.app_context():
    db.create_all()

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
