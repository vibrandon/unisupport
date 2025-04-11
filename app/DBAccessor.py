import sqlalchemy as sa
import sqlalchemy.exc
from app import app,db
from app.models import User, Professional, Student
from datetime import date, datetime
class StudentSurvey:
    pass
class DBAccessor:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBAccessor, cls).__new__(cls)
        return cls._instance
    def query_student_by_id(self,id):
        student = db.session.scalar(db.select(Student).where(Student.id==id))
        return student
    def match_professional(self,sid,pid):
        student = db.session.scalar(db.select(Student).where(Student.id==sid))
        student.pid = pid
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            db.session.rollback()
    def student_survey(self,current_user):
        try:
            survey = studentSurvey(
                student=current_user,
                studentID=current_user.id,
                timestamp=datetime.now(),
                questions={}
            )
            #change questions from a list into a dictionary with {question:answer,question:answer} pairs
            db.session.add(survey)
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            db.session.rollback()