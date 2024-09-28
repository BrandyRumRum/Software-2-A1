from App.models import Staff
from App.database import db

def create_staff(name, role):
    staff = Staff(name=name, role=role)
    db.session.add(staff)
    db.session.commit()
    print(name + " has been created and assigned to " + role)