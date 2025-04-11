from app import db
from app.models import (
    User, Student, Professional, Message, Admin,
    studentSurvey, professionalSurvey, wellbeingProfile
)
from werkzeug.security import generate_password_hash

def reset_db():
    db.drop_all()
    db.create_all()

    admin = Admin(
        username="admin",
        firstname="Admin",
        lastname="User",
        email="admin@unisupport.com",
        role="Admin",
        type="admin"
    )
    admin.set_password("adminpass")
    db.session.add(admin)

    professionals = []
    for i in range(5):
        p = Professional(
            username=f"pro{i+1}",
            firstname=f"Pro{i+1}",
            lastname="Smith",
            email=f"pro{i+1}@unisupport.com",
            phoneNumber=f"000000000{i+1}",
            workplace=f"Workplace {i+1}",
            specialty="Stress Management",
            role="professional",
            type="professional"
        )
        p.set_password("password")
        professionals.append(p)
    db.session.add_all(professionals)

    students = []
    for i in range(10):
        s = Student(
            username=f"student{i+1}",
            firstname=f"Student{i+1}",
            lastname="Doe",
            email=f"student{i+1}@student.com",
            phoneNumber=f"111111111{i+1}",
            address=f"Dorm {i+1}A",
            degree="Computer Science",
            role="student",
            type="student"
        )
        s.set_password("password")
        students.append(s)
    db.session.add_all(students)
    db.session.commit()

    # Example message between first student and professional
    db.session.add_all([
        Message(sender_id=students[0].id, receiver_id=professionals[0].id, content="Hi, I need help."),
        Message(sender_id=professionals[0].id, receiver_id=students[0].id, content="Of course! I'm here to help.")
    ])

    db.session.commit()
    print("✅ Database has been reset and seeded.")
