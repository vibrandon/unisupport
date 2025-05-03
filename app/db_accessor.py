import sqlalchemy.exc
from flask import flash

from app import app,db
from app.models import User, Professional, Student, studentSurvey, wellbeingProfile, StudentChatMessage
from datetime import date, datetime

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
    def record_student_survey(self,current_user,questions):
        #copy in updated student survey
        try:
            survey = studentSurvey(
                id=current_user.id,
                student=current_user,
                studentID=current_user.id,
                timestamp=datetime.now(),
                questions=questions
            )
            #change questions from a list into a dictionary with {question:answer,question:answer} pairs
            db.session.add(survey)
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            db.session.rollback()
            raise sqlalchemy.exc.SQLAlchemyError()
            flash(f"{e} occurred", "danger")
    def update_wellbeing_profile(self,user,wellbeing_status,wellbeing_score,recommendations_csv):
        if user.wellbeingProfile:
            user.wellbeingProfile.wellbeingStatus = wellbeing_status
            user.wellbeingProfile.wellbeingScore = wellbeing_score
            user.wellbeingProfile.recommendations = recommendations_csv
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(f"Error: {str(e)}", "danger")
    def new_wellbeing_profile(self,user,wellbeing_status,wellbeing_score,recommendations_csv):
        new_well_profile = wellbeingProfile(
            student=user,
            studentID=user.id,
            wellbeingStatus=wellbeing_status,
            wellbeingScore=wellbeing_score,
            recommendations=recommendations_csv
        )
        try:
            db.session.add(new_well_profile)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

    def get_all_professionals(self):
        return db.session.scalars(db.select(Professional)).all()

    def get_all_students(self):
        return db.session.scalars(db.select(Student)).all()

    def get_user_by_id(self, user_id):
        return db.session.get(User, user_id)

    def add_message(self, message):
        try:
            db.session.add(message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

    def add_student_message(self, message):
        db.session.add(message)
        db.session.commit()

    def get_recent_student_messages(self, limit=50):
        return StudentChatMessage.query.order_by(StudentChatMessage.timestamp.desc()).limit(limit).all()
