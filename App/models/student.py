from App.database import db

class Student(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"<Student ID= {self.id:<3}  Name= {self.name:<20} Email= {self.email}>"
    