from pytest_bdd import scenarios, given, when, then, parsers
from app import app,db
import pytest
from app.db_accessor import DBAccessor
from app.models import Student
from flask_sqlalchemy import SQLAlchemy
scenarios('./features/matching.feature')

@pytest.fixture
def system():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()
    return app
# the first test case: student match a professional
@given(parsers.parse('a student whose id is {student_id}'),target_fixture="student")
def student(system):
    student1 = Student(
        username=f"student1",
        firstname=f"Student1",
        lastname="Doe",
        email=f"student@student.com",
        phoneNumber=f"1111111111",
        address=f"Dorm 1A",
        degree="Computer Science",
        role="student",
        type="student"
    )
    db.session.add(student1)
    db.session.commit()
    return student1

@when(parsers.parse('the student chooses a professional whose id is {professional_id:d} as his preferred professional'))
def match_student_id_with_professional_id(student, professional_id):
    db_accessor = DBAccessor()
    flag = db_accessor.match_professional(student.id, professional_id)
    assert flag == True

@then(parsers.parse('his preferred professional id is {professional_id:d}'))
def check_preferred_professional_id(student,professional_id):
    db_accessor = DBAccessor()
    user = db_accessor.query_student_by_id(student.id)
    assert user.pid == professional_id 

# the second test case: a student doesnot provide a professional id 
@given(parsers.parse('a student'),target_fixture="student")
def student(system):
    student1 = Student(
        username=f"student1",
        firstname=f"Student1",
        lastname="Doe",
        email=f"student@student.com",
        phoneNumber=f"1111111111",
        address=f"Dorm 1A",
        degree="Computer Science",
        role="student",
        type="student"
    )
    db.session.add(student1)
    db.session.commit()
    return student1
@when(parsers.parse("the student does not provide a professional id"))
def no_professional_id_provided():
    pass

@then(parsers.parse('the system return false'))
def please_provide_a_name(student):
    db_accessor = DBAccessor()
    flag = db_accessor.match_professional(student.id, '')
    assert flag == False