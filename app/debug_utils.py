def reset_db():
    from app.models import User, Professional, Message, AdjustmentRequest
    from app import db

    # 🔥 Wipe everything
    db.drop_all()
    db.create_all()

    # 👤 Users
    u1 = User(username='amy', firstname='Amy', lastname='Smith', email='a@b.com', role='Admin', address='123 Campus Way')
    u1.set_password('amy.pw')
    u2 = User(username='tom', firstname='Tom', lastname='Lee', email='t@b.com', address='Dorm 7')
    u2.set_password('tom.pw')
    u3 = User(username='yin', firstname='Yin', lastname='Chen', email='y@b.com', role='Admin', address='Off-campus')
    u3.set_password('yin.pw')
    u4 = User(username='tariq', firstname='Tariq', lastname='Hassan', email='tariq@b.com')
    u4.set_password('tariq.pw')
    u5 = User(username='jo', firstname='Jo', lastname='Jones', email='jo@b.com')
    u5.set_password('jo.pw')

    # 👨‍⚕️ Professionals
    p1 = Professional(name="Dr. Alice Bennett", specialty="Therapist", email="alice@unicare.com")
    p2 = Professional(name="Mr. Ben Carter", specialty="Academic Advisor", email="ben@unicare.com")

    # 📩 Messages
    m1 = Message(sender_id=1, recipient_id=2, content="Hi, how do I request an extension?")
    m2 = Message(sender_id=2, recipient_id=1, content="Sure! Use the 'Adjustments' section.")

    # 📄 Adjustment Requests
    ar1 = AdjustmentRequest(user_id=2, reason="Mental health reasons affecting assignment deadlines.")
    ar2 = AdjustmentRequest(user_id=5, reason="Unexpected family emergency.")

    db.session.add_all([u1, u2, u3, u4, u5, p1, p2, m1, m2, ar1, ar2])
    db.session.commit()

    print("✅ Database reset complete — users, professionals, messages, and adjustment requests seeded.")

