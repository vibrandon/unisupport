def reset_db():
    from app import db
    from app.models import Student, Professional

    # 🔥 Reset database
    db.drop_all()
    db.create_all()

    # 👨‍⚕️ Professionals
    p1 = Professional(
        username='drsmith',
        firstname='John',
        lastname='Smith',
        email='john.smith@unisupport.com',
        phone_number='1234567890',
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
        phone_number='0987654321',
        workplace='Health Services',
        specialty='Time Management, Burnout',
        role='professional',
        type='professional'
    )
    p2.set_password('janepass')

    db.session.add_all([p1, p2])
    db.session.commit()

    # 🎓 Students
    s1 = Student(
        username='alice',
        firstname='Alice',
        lastname='Green',
        email='alice@student.com',
        phone_number='1112223333',
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
        phone_number='2223334444',
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
        phone_number='3334445555',
        address='Dorm 16C',
        degree='Engineering',
        role='student',
        type='student'
    )
    s3.set_password('charliepw')

    db.session.add_all([s1, s2, s3])
    db.session.commit()

    print("✅ Database reset complete — professionals and students seeded.")
