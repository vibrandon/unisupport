# Import sys module for modifying Python's runtime environment
import sys
# Import os module for interacting with the operating system
import os

# Import the Flask app instance from the main app file
from app import app
from app.models import Student
from app.DBAccessor import DBAccessor
# Import pytest for writing and running tests
import pytest

@pytest.fixture
def app_context():
    with app.app_context():
        yield 

def test_query_student_by_id(app_context):
    instance = DBAccessor()
    student = instance.query_student_by_id(id=7)
    assert student.id== 1

def test_match_professional(app_context):
    instance = DBAccessor()
    instance.match_professional(sid=7 , pid=1)
    student = instance.query_student_by_id(id=7)
    assert student.pid== 1