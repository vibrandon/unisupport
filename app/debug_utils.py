def reset_db():
    from app import db
    from app.models import Student, Professional, User, Message
    from datetime import datetime

    db.drop_all()
    db.create_all()

    # 👨‍⚕️ Professionals
    professionals = [
        Professional(username='drsmith', firstname='John', lastname='Smith', email='john.smith@unisupport.com', phoneNumber='1234567890', workplace='UoB Counseling Center', specialty='Anxiety, Depression, Stress', role='professional', type='professional'),
        Professional(username='drjane', firstname='Jane', lastname='Doe', email='jane.doe@unisupport.com', phoneNumber='0987654321', workplace='Health Services', specialty='Time Management, Burnout', role='professional', type='professional'),
        Professional(username='drlee', firstname='Daniel', lastname='Lee', email='daniel.lee@unisupport.com', phoneNumber='9998887777', workplace='Student Wellness', specialty='Academic Stress, Life Balance', role='professional', type='professional'),
        Professional(username='drkhan', firstname='Sara', lastname='Khan', email='sara.khan@unisupport.com', phoneNumber='4443332211', workplace='Mental Health Center', specialty='Social Anxiety, Adjustment', role='professional', type='professional'),
        Professional(username='drchan', firstname='Brian', lastname='Chan', email='brian.chan@unisupport.com', phoneNumber='7778889999', workplace='Student Counseling Hub', specialty='Self-esteem, Motivation', role='professional', type='professional'),
    ]
    for p in professionals:
        p.set_password('testpass')

    db.session.add_all(professionals)
    db.session.commit()

    # 🎓 Students
    students = [
        Student(username='alice', firstname='Alice', lastname='Green', email='alice@student.com', phoneNumber='1112223333', address='Dorm 12A', degree='Computer Science', role='student', type='student'),
        Student(username='bob', firstname='Bob', lastname='Brown', email='bob@student.com', phoneNumber='2223334444', address='Dorm 14B', degree='Psychology', role='student', type='student'),
        Student(username='charlie', firstname='Charlie', lastname='Black', email='charlie@student.com', phoneNumber='3334445555', address='Dorm 16C', degree='Engineering', role='student', type='student'),
        Student(username='diana', firstname='Diana', lastname='White', email='diana@student.com', phoneNumber='4445556666', address='Dorm 18A', degree='Mathematics', role='student', type='student'),
        Student(username='ethan', firstname='Ethan', lastname='Gray', email='ethan@student.com', phoneNumber='5556667777', address='Dorm 20B', degree='Economics', role='student', type='student'),
        Student(username='fiona', firstname='Fiona', lastname='Lee', email='fiona@student.com', phoneNumber='6667778888', address='Dorm 22C', degree='Biology', role='student', type='student'),
        Student(username='george', firstname='George', lastname='Taylor', email='george@student.com', phoneNumber='7778889990', address='Dorm 24D', degree='Chemistry', role='student', type='student'),
        Student(username='hannah', firstname='Hannah', lastname='Wright', email='hannah@student.com', phoneNumber='8889990001', address='Dorm 26E', degree='Philosophy', role='student', type='student'),
        Student(username='ian', firstname='Ian', lastname='King', email='ian@student.com', phoneNumber='9990001112', address='Dorm 28F', degree='Business', role='student', type='student'),
        Student(username='julia', firstname='Julia', lastname='Scott', email='julia@student.com', phoneNumber='0001112223', address='Dorm 30G', degree='English Literature', role='student', type='student'),
    ]
    for s in students:
        s.set_password('studentpw')

    db.session.add_all(students)
    db.session.commit()

    # 🛡 Admin
    admin = User(
        username='admin',
        firstname='Admin',
        lastname='User',
        email='admin@unisupport.com',
        role='Admin',
        type='user'  # base user
    )
    admin.set_password('adminpass')

    db.session.add(admin)
    db.session.commit()

    # 💬 Sample Messages
    messages = [
        Message(sender_id=students[0].id, receiver_id=professionals[0].id,
                content="Hi, I’m struggling with anxiety. Can we talk?"),
        Message(sender_id=professionals[0].id, receiver_id=students[0].id,
                content="Absolutely, I'm here for you. How long have you been feeling this way?"),

        Message(sender_id=students[1].id, receiver_id=professionals[1].id,
                content="I'm feeling overwhelmed with my workload."),
        Message(sender_id=professionals[1].id, receiver_id=students[1].id,
                content="That’s totally understandable. Let’s explore some time management strategies."),

        Message(sender_id=students[2].id, receiver_id=professionals[2].id,
                content="Do you help with imposter syndrome?"),
        Message(sender_id=professionals[2].id, receiver_id=students[2].id,
                content="Yes, that's very common — and absolutely something I can support you with."),

        Message(sender_id=students[3].id, receiver_id=professionals[3].id,
                content="I feel like I'm behind compared to my peers."),
        Message(sender_id=professionals[3].id, receiver_id=students[3].id,
                content="You're not alone in that feeling. Let’s reframe it together."),

        Message(sender_id=students[4].id, receiver_id=professionals[4].id, content="I’m anxious about exams."),
        Message(sender_id=professionals[4].id, receiver_id=students[4].id,
                content="Thanks for sharing that — let's work on some calming techniques."),
    ]

    db.session.add_all(messages)
    db.session.commit()

    print("✅ Database reset complete — 10 students, 5 professionals, and 1 admin seeded.")
