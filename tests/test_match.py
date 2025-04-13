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

def test_match_professional(app_context):
    instance = DBAccessor()
    instance.match_professional(sid=4 , pid=1)
    student = instance.query_student_by_id(id=4)
    assert student.pid== 1