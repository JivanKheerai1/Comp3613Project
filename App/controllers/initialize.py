from App.models import Student, Staff
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    #create_user('bob', 'bobpass')

    # Add sample students
    students = [
        Student(name='Alice', email='alice@example.com'),
        Student(name='Bob', email='bob@example.com'),
        Student(name='Charlie', email='charlie@example.com'),
        Student(name='Diana', email='diana@example.com'),
        Student(name='Eve', email='eve@example.com'),
        Student(name='Frank', email='frank@example.com'),
    ]
    db.session.add_all(students)

    staff = Staff(name='Mr. Smith', email='smith@example.com')
    db.session.add(staff)
    db.session.commit()
