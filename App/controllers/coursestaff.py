from App.models import CourseStaff, Course, Staff
from App.database import db

def assign_staff(course_name, staff_name):
    course = Course.query.filter_by(name=course_name).first()
    staff = Staff.query.filter_by(name=staff_name).first()

    if not course or not staff:
        print("Cannot make assignment")
        return

    course_staff = CourseStaff(course_id=course.id, staff_id=staff.id)
    db.session.add(course_staff)
    db.session.commit()
    print("Staff member " + staff_name + " has been assigned to " + course_name)

def view_course_staff(course_name):
    course = Course.query.filter_by(name=course_name).first()
    
    if not course:
        print('Course not found.')
        return
    
    staff = course.course_staff
    if not staff:
        print('No staff members are assigned to this course.')
        return
    
    print(f'Staff for course "{course.name}":')
    for staff_members in staff:
        print(f'{staff_members.staff.name} ({staff_members.staff.role})')