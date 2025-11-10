import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    resource_type = db.Column(db.String(50))
    course = db.Column(db.String(50))
    year = db.Column(db.String(10))
    semester = db.Column(db.String(10))
    exam_type = db.Column(db.String(50))
    filepath = db.Column(db.String(300))
    uploaded_by = db.Column(db.Integer)  
    upload_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<File {self.filename} - {self.course}>"
