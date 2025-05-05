from app import db
from app.models import (
    User, Student, Professional, Message, Admin,
    studentSurvey, professionalSurvey, wellbeingProfile, StudentChatMessage
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
    pro_names = [
        ("Emma", "Johnson"),
        ("Liam", "Williams"),
        ("Olivia", "Brown"),
        ("Noah", "Jones"),
        ("Ava", "Garcia")
    ]
    for i, (first, last) in enumerate(pro_names):
        p = Professional(
            username=f"pro{i + 1}",
            firstname=first,
            lastname=last,
            email=f"{first.lower()}.{last.lower()}@unisupport.com",
            phoneNumber=f"000000000{i + 1}",
            workplace=f"Wellbeing Center {i + 1}",
            specialty="Stress Management",
            role="professional",
            type="professional"
        )
        p.set_password("password")
        professionals.append(p)
    db.session.add_all(professionals)

    students = []
    student_names = [
        ("James", "Miller"),
        ("Sophia", "Davis"),
        ("Benjamin", "Martinez"),
        ("Isabella", "Hernandez"),
        ("Lucas", "Lopez"),
        ("Mia", "Gonzalez"),
        ("Henry", "Wilson"),
        ("Charlotte", "Anderson"),
        ("Alexander", "Thomas"),
        ("Amelia", "Taylor")
    ]
    student_degrees = [
        "Computer Science",
        "Psychology",
        "Mechanical Engineering",
        "Business Management",
        "Biology",
        "Sociology",
        "Electrical Engineering",
        "Political Science",
        "Economics",
        "English Literature"
    ]
    for i, (first, last) in enumerate(student_names):
        s = Student(
            username=f"student{i + 1}",
            firstname=first,
            lastname=last,
            email=f"{first.lower()}.{last.lower()}@student.com",
            phoneNumber=f"111111111{i + 1}",
            address=f"Dorm {i + 1}A",
            degree=student_degrees[i],
            role="student",
            type="student"
        )
        s.set_password("password")
        students.append(s)
    db.session.add_all(students)

    db.session.commit()

    # Example message between first student and professional
    messages = []
    pair_count = min(len(professionals), len(students))
    for i in range(pair_count):
        messages.append(Message(
            sender_id=professionals[i].id,
            receiver_id=students[i].id,
            content=f"Hi {students[i].firstname}, you've been matched with me, {professionals[i].firstname}, for support!"
        ))
        messages.append(Message(
            sender_id=students[i].id,
            receiver_id=professionals[i].id,
            content="Thank you for the support"
        ))
    db.session.add_all(messages)

    unique_student_messages = [
        "Hey everyone! Anyone up for a study group this weekend?",
        "Just finished the project — feeling relieved!",
        "Struggling a bit with the algorithms homework, anyone else?",
        "Looking for a good coffee spot on campus, recommendations?",
        "Has anyone tried the new note-taking app?",
        "Excited for the coding bootcamp next month!",
        "Feeling overwhelmed, but trying to stay positive.",
        "Anyone want to swap lecture notes?",
        "Ready for the group presentation next week!",
        "Just joined the chat — hi all!"
    ]

    open_chat_messages = []
    for i, student in enumerate(students):
        open_chat_messages.append(StudentChatMessage(
            sender_id=student.id,
            content=unique_student_messages[i]
        ))
    db.session.add_all(open_chat_messages)

    db.session.commit()
    print("✅ Database has been reset")
