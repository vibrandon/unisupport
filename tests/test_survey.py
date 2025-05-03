import pytest
import sqlalchemy.exc

from app import db, app
from app.db_accessor import DBAccessor
from app.models import Student, studentSurvey


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

    return app

@pytest.fixture
def student():
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
    # delete all surveys matching that student's ID in the database
    db.session.commit()
    return student1

def test_record_student_survey(client,student):
    db_accessor = DBAccessor()
    user = db_accessor.query_student_by_id(1)

    # delete all surveys matching that student's ID in the database
    # Given a Student currently has 0 surveys,
    if user.surveys:
        print("debug\n" * 20)
        for survey in user.surveys:
            db.session.delete(survey)
            db.session.commit()

    # When a survey with a bad questions parameter is added to the database using DBAccessor.record_student_survey()
    #Then an exception should be thrown
    with pytest.raises(sqlalchemy.exc.SQLAlchemyError) as e:
        with app.app_context():
            db_accessor.record_student_survey(
                current_user=user,
                questions={}
            )

    #And then the survey should NOT have been added to the database
    surveys_query = db.select(studentSurvey).where(Student==user)
    user_surveys = db.session.scalars(surveys_query).all()
    print(user_surveys)
    #query for surveys matching that student returns empty List.
    assert user_surveys == []
