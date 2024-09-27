from App.database import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Lecturer, TA, Tutor

    def __init__(self, name, role):
        self.name = name
        self.role = role