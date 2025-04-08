def reset_db():
    from app import db
    from app.models import Student, Professional

    # 🔥 Drop & recreate all tables
    db.drop_all()
    db.create_all()

    # # 👨‍⚕️ Professionals
    # p1 = Professional(
    #     username='drsmith',
    #     firstname='John',
    #     lastname='Smith',
    #     email='john.smith@unisupport.com',
    #     phoneNumber='1234567890',
    #     workplace='UoB Counseling Center',
    #     expertise='Anxiety, Stress, Exam Pressure',
    #     userType='professional'
    # )
    # p1.set_password('smithpass')
    #
    # p2 = Professional(
    #     username='drjane',
    #     firstname='Jane',
    #     lastname='Doe',
    #     email='jane.doe@unisupport.com',
    #     phoneNumber='0987654321',
    #     workplace='Health Services',
    #     expertise='Time Management, Burnout',
    #     userType='professional'
    # )
    # p2.set_password('janepass')
    #
    # db.session.add_all([p1, p2])
    # db.session.commit()  # Commit now so we have p1.id and p2.id for foreign keys

    # 🎓 Students assigned to professionals
    s1 = Student(
        username='alice',
        firstname='Alice',
        lastname='Green',
        email='alice@student.com',
        phoneNumber='1112223333',
        degree='Computer Science',
        address='Dorm 7A',
        userType='student'
    )
    s1.set_password('alicepw')

    s2 = Student(
        username='bob',
        firstname='Bob',
        lastname='Brown',
        email='bob@student.com',
        phoneNumber='2223334444',
        degree='Psychology',
        address='Dorm 5B',
        userType='student'
    )
    s2.set_password('bobpw')

    s3 = Student(
        username='charlie',
        firstname='Charlie',
        lastname='Black',
        email='charlie@student.com',
        phoneNumber='3334445555',
        degree='Engineering',
        address='Dorm 10C',
        userType='student'
    )
    s3.set_password('charliepw')

    db.session.add_all([s1, s2, s3])
    db.session.commit()

    print("✅ Database reset complete — professionals and students seeded.")
