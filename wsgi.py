import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import *
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)


def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    setup_admin(app)
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401
    app.app_context().push()
    return app

# Staff members can create their own account
staff_cli = AppGroup('staff', help='Staff object commands')

# Command to create a staff member
@staff_cli.command('create-staff')
def create_staff():
    name = input('Enter staff name: ')
    role = input('Enter staff role (Lecturer, TA, Tutor): ')
    staff = Staff(name=name, role=role)
    db.session.add(staff)
    db.session.commit()
    print(f'Staff member "{name}" with role "{role}" created successfully.')

app.cli.add_command(staff_cli)

# Admins can create courses and assign staff to them
admin_cli = AppGroup('admin', help='Admin object commands') 

@admin_cli.command('create-course')
def create_course():
    name = input('Enter course name: ')
    course = Course(name=name)
    db.session.add(course)
    db.session.commit()
    print(f'Course "{name}" created successfully.')


# Command to assign staff to a course
@admin_cli.command('assign-staff')
def assign_staff():
    course_id = int(input('Enter course ID: '))
    staff_id = int(input('Enter staff ID: '))
    assignment = CourseStaff(course_id=course_id, staff_id=staff_id)
    db.session.add(assignment)
    db.session.commit()
    print(f'Staff ID "{staff_id}" assigned to Course ID "{course_id}".')

# Command to view course staff
@admin_cli.command('view-course-staff')
def view_course_staff():
    course_id = int(input('Enter course ID: '))
    course = Course.query.get(course_id)
    if not course:
        print('Course not found.')
        return
    staff_members = course.course_staff
    if not staff_members:
        print('No staff assigned to this course.')
        return
    print(f'Staff for course "{course.name}":')
    for cs in staff_members:
        print(f'- {cs.staff.name} ({cs.staff.role})')

app.cli.add_command(admin_cli)


if __name__ == '__main__':
    app.run(debug=True)