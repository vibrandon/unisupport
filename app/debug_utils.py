def reset_db():
    from app import db
    from app.models import Student, Professional, User

    # 🔥 Reset database
    db.drop_all()
    db.create_all()

    # 👨‍⚕️ Professionals
    p1 = Professional(
        username='drsmith',
        firstname='John',
        lastname='Smith',
        email='john.smith@unisupport.com',
        phoneNumber='1234567890',
        workplace='UoB Counseling Center',
        specialty='Anxiety, Depression, Stress',
        role='professional',
        type='professional'
    )
    p1.set_password('smithpass')

    p2 = Professional(
        username='drjane',
        firstname='Jane',
        lastname='Doe',
        email='jane.doe@unisupport.com',
        phoneNumber='0987654321',
        workplace='Health Services',
        specialty='Time Management, Burnout',
        role='professional',
        type='professional'
    )
    p2.set_password('janepass')

    p3 = Professional(
        username='drlee',
        firstname='Daniel',
        lastname='Lee',
        email='daniel.lee@unisupport.com',
        phoneNumber='9998887777',
        workplace='Student Wellness',
        specialty='Academic Stress, Life Balance',
        role='professional',
        type='professional'
    )
    p3.set_password('leepass')

    db.session.add_all([p1, p2, p3])
    db.session.commit()

    # 🎓 Students
    s1 = Student(
        username='alice',
        firstname='Alice',
        lastname='Green',
        email='alice@student.com',
        phoneNumber='1112223333',
        address='Dorm 12A',
        degree='Computer Science',
        role='student',
        type='student'
    )
    s1.set_password('alicepw')

    s2 = Student(
        username='bob',
        firstname='Bob',
        lastname='Brown',
        email='bob@student.com',
        phoneNumber='2223334444',
        address='Dorm 14B',
        degree='Psychology',
        role='student',
        type='student'
    )
    s2.set_password('bobpw')

    s3 = Student(
        username='charlie',
        firstname='Charlie',
        lastname='Black',
        email='charlie@student.com',
        phoneNumber='3334445555',
        address='Dorm 16C',
        degree='Engineering',
        role='student',
        type='student'
    )
    s3.set_password('charliepw')

    s4 = Student(
        username='diana',
        firstname='Diana',
        lastname='White',
        email='diana@student.com',
        phoneNumber='4445556666',
        address='Dorm 18A',
        degree='Mathematics',
        role='student',
        type='student'
    )
    s4.set_password('dianapw')

    s5 = Student(
        username='ethan',
        firstname='Ethan',
        lastname='Gray',
        email='ethan@student.com',
        phoneNumber='5556667777',
        address='Dorm 20B',
        degree='Economics',
        role='student',
        type='student'
    )
    s5.set_password('ethanpw')

    db.session.add_all([s1, s2, s3, s4, s5])
    db.session.commit()


    admin = User(
        username='admin',
        firstname='Admin',
        lastname='User',
        email='admin@unisupport.com',
        role='Admin',
        type='user'  # base user, not student/professional
    )
    admin.set_password('adminpass')

    db.session.add(admin)
    db.session.commit()

    print("✅ Database reset complete — professionals and students seeded.")
