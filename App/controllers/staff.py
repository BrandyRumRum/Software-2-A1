from App.models import Staff
from App.database import db

def create_staff(name, role):
    existing_staff = Staff.query.filter_by(name=name, role=role).first()
    if existing_staff:
        print(name + " the " + role + " already exists")
        return
    

    staff_member = Staff(name=name, role=role)
    try:
        db.session.add(staff_member)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print("Staff member already exists")
    else:
        print(name + " the " + role + " has been created")


    