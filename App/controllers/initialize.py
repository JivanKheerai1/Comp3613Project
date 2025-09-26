from App.models import Student, Staff, Request
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
        Student(name='Grace', email='grace@example.com'),
        Student(name='Heidi', email='heidi@example.com'),
        Student(name='Ivan', email='ivan@example.com'),
        Student(name='Judy', email='judy@example.com'),
        Student(name='Karl', email='karl@example.com'),
        Student(name='Liam', email='liam@example.com'),
        Student(name='Mallory', email='mallory@example.com'),
        Student(name='Niaj', email='niaj@example.com'),
        Student(name='Olivia', email='olivia@example.com'),
        Student(name='Peggy', email='peggy@example.com'),
    ]
    db.session.add_all(students)
    db.session.commit()


    staff_members = [
        Staff(name='Mr. Smith', email='smith@example.com'),
        Staff(name='Ms. Johnson', email='johnson@example.com'),
        Staff(name='Mr. Lee', email='lee@example.com'),
        Staff(name='Ms. Patel', email='patel@example.com'),
        Staff(name='Mr. Brown', email='brown@example.com'),
        
    ]
    for staff_member in staff_members:
        db.session.add(staff_member)
    db.session.commit()


    # Add 10 sample requests for students (not random)
    
    all_students = Student.query.order_by(Student.id).all()
    requests = []
    for i, student in enumerate(all_students[:10]):
        hours = 10 * (i + 1)  # 10, 20, ..., 100
        req = Request(student_id=student.id, hours=hours, status='pending')
        requests.append(req)
    db.session.add_all(requests)
    db.session.commit()



    # Let some staff members approve some requests

    all_staff = Staff.query.order_by(Staff.id).all()
    # Approve first 5 requests by first 5 staff (if enough staff exist)
    for i, req in enumerate(requests[:5]):
        staff_member = all_staff[i % len(all_staff)]
        staff_member.approve_request(req)
