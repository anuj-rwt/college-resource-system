from models import db
import datetime

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    resource_type = db.Column(db.String(100))
    course = db.Column(db.String(100))
    year = db.Column(db.String(20))
    semester = db.Column(db.String(20))
    exam_type = db.Column(db.String(50))
    upload_time = db.Column(db.String(50), default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __init__(self, filename, filepath, uploaded_by, resource_type=None, course=None, year=None, semester=None, exam_type=None):
        self.filename = filename
        self.filepath = filepath
        self.uploaded_by = uploaded_by
        self.resource_type = resource_type
        self.course = course
        self.year = year
        self.semester = semester
        self.exam_type = exam_type

