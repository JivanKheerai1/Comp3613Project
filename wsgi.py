import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.models import Student
from App.models import Staff
from App.models import Request
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


'''APP COMMANDS(TESTING PURPOSES)'''

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')


#Comamand to list all staff in the database
@app.cli.command ("listStaff", help="Lists all staff in the database")
def listStaff():
    staff = Staff.query.all()
    for member in staff:
        print(member)


#Comamand to list all students in the database
@app.cli.command ("listStudents", help="Lists all students in the database")
def listStudents():
    students = Student.query.all()
    for student in students:
        print(student)


#Comamand to list all requests in the database
@app.cli.command ("listRequests", help="Lists all requests in the database")
def listRequests():
    requests = Request.query.all()
    for request in requests:
        print(request)


#Comamand to list all approved requests in the database
@app.cli.command ("listApprovedRequests", help="Lists all approved requests in the database")
def listApprovedRequests():
    requests = Request.query.filter_by(status='approved').all()
    for request in requests:
        print(request)


#Comamand to list all pending requests in the database
@app.cli.command ("listPendingRequests", help="Lists all pending requests in the database")
def listPendingRequests():
    requests = Request.query.filter_by(status='pending').all()
    for request in requests:
        print(request)


#Comamand to list all denied requests in the database
@app.cli.command ("listDeniedRequests", help="Lists all denied requests in the database")
def listDeniedRequests():
    requests = Request.query.filter_by(status='denied').all()
    for request in requests:
        print(request)


#Comamand to list all logged hours in the database
@app.cli.command ("listloggedHours", help="Lists all logged hours in the database")
def listloggedHours():
    from App.models import LoggedHours
    logs = LoggedHours.query.all()
    for log in logs:
        print(log)



'''STUDENT COMMANDS'''

student_cli = AppGroup('student', help='Student object commands')

@student_cli.command("listStudents", help="Lists all students in the database")
def listStudents():
    students = Student.query.all()
    for student in students:
        print(student)



#Command for student to request hour confirmation (student_id, hours)
@student_cli.command("requestHours", help="Student requests hour confirmation")
@click.argument("student_id", type=int)
@click.argument("hours", type=float)
def requestHours(student_id, hours):
    student = Student.query.get(student_id)
    if not student:
        print(f"Student with id {student_id} not found.")
        return
    req = student.request_hours_confirmation(hours)
    print(f"Requested {hours} hours for confirmation. Request ID: {req.id}, Status: {req.status}")


#command to list all requests made by a specific student(student_id)
@student_cli.command("listRequests", help="List all requests for a student")
@click.argument("student_id", type=int)
def listRequests(student_id):
    from App.models import Request
    student = Student.query.get(student_id)
    if not student:
        print(f"Student with id {student_id} not found.")
        return
    if not student.requests:
        print(f"No requests found for student {student_id}.")
    for req in student.requests:
        print(req)


#command to list all accolades for a specific student (student_id)
@student_cli.command("listAccolades", help="List all accolades for a student")
@click.argument("student_id", type=int)
def listAccolades(student_id):
    student = Student.query.get(student_id)
    if not student:
        print(f"Student with id {student_id} not found.")
        return
    accolades = student.accolades()
    if not accolades:
        print(f"No accolades found for student {student_id}.")
    else:
        print(f"Accolades for student {student_id}:")
        for accolade in accolades:
            print(f"- {accolade}")


#Student command to view leaderboard of students by approved hours
@student_cli.command("viewLeaderboard", help="View leaderboard of students by approved hours")
def viewLeaderboard():
    students = Student.query.all()
    leaderboard = sorted(students, key=lambda s: sum(lh.hours for lh in s.loggedhours if lh.status == 'approved'), reverse=True)
    print("Leaderboard (by approved hours):")
    for rank, student in enumerate(leaderboard, 1):
        total_hours = sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')
        print(f"{rank:<6}. {student.name:<10} ------ \t{total_hours} hours")


app.cli.add_command(student_cli) # add the group to the cli




'''STAFF COMMANDS'''



staff_cli = AppGroup('staff', help='Staff object commands')

#Command for staff to approve a student's request (staff_id, request_id)
#Once approved it is added to logged hours database
@staff_cli.command("approveRequest", help="Staff approves a student's request")
@click.argument("staff_id", type=int)
@click.argument("request_id", type=int)
def approveRequest(staff_id, request_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        print(f"Staff with id {staff_id} not found.")
        return
    request = Request.query.get(request_id)
    if not request:
        print(f"Request with id {request_id} not found.")
        return
    student = Student.query.get(request.student_id)
    student_name = student.name 
    logged = staff.approve_request(request)
    if logged:
        print(f"Request {request_id} for {request.hours} hours made by {student_name} approved by Staff {staff.name} (ID: {staff_id}). Logged Hours ID: {logged.id}")
    else:
        print(f"Request {request_id} for {request.hours} hours made by {student_name} could not be approved (Already Processed).")





# Command for staff to deny a student's request (staff_id, request_id)
#change request status to denied, no logged hours created
@staff_cli.command("denyRequest", help="Staff denies a student's request") 
@click.argument("staff_id", type=int)
@click.argument("request_id", type=int)
def denyRequest(staff_id, request_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        print(f"Staff with id {staff_id} not found.")
        return
    request = Request.query.get(request_id)
    if not request:
        print(f"Request with id {request_id} not found.")
        return
    student = Student.query.get(request.student_id)
    student_name = student.name
    success = staff.deny_request(request)
    if success:
        print(f"Request {request_id} for {request.hours} hours made by {student_name} denied by Staff {staff.name} (ID: {staff_id}).")
    else:
        print(f"Request {request_id} for {request.hours} hours made by {student_name} could not be denied (Already Processed).")



#staff command to view leaderboard of students by approved hours
@staff_cli.command("viewLeaderboard", help="View leaderboard of students by approved hours")
def viewLeaderboard():
    students = Student.query.all()
    leaderboard = sorted(students, key=lambda s: sum(lh.hours for lh in s.loggedhours if lh.status == 'approved'), reverse=True)
    print("Leaderboard (by approved hours):")
    for rank, student in enumerate(leaderboard, 1):
        total_hours = sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')
        print(f"{rank:<6}. {student.name:<10} ------ \t{total_hours} hours")

app.cli.add_command(staff_cli) # add the group to the cli