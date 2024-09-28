from App.models import Course
from App.database import db

def create_course(name):
    course = Course(name=name)
    db.session.add(course)
    db.session.commit()
    print(name + " has been created")