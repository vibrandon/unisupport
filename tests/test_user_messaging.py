import logging

logging.disable(logging.CRITICAL)

import pytest
from app import app, db
from app.models import User


@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def sample_users():
    user1 = User(
        username='user1',
        firstname='First',
        lastname='User',
        email='user1@example.com',
        phoneNumber='1234567890',
        role='student',
        type='user',
        password_hash='hashed_password'
    )
    user2 = User(
        username='user2',
        firstname='Second',
        lastname='User',
        email='user2@example.com',
        phoneNumber='0987654321',
        role='student',
        type='user',
        password_hash='hashed_password'
    )
    db.session.add_all([user1, user2])
    db.session.commit()
    return user1, user2


#Testing for chat with existing user
def test_chat_with_existing_user(test_client, sample_users):
    user1, user2 = sample_users
    with test_client.session_transaction() as sess:
        sess['_user_id'] = str(user1.id)

    response = test_client.get(f'/userMessaging/{user2.id}')
    assert response.status_code == 200
    assert b"Chat" in response.data


#Testing for chat with a user that doesn't exist
def test_chat_with_nonexistent_user(test_client, sample_users):
    user1, _ = sample_users
    with test_client.session_transaction() as sess:
        sess['_user_id'] = str(user1.id)

    response = test_client.get('/userMessaging/999', follow_redirects=True)
    assert response.status_code in (200, 404)
    assert b"User not found" in response.data or b"No such user" in response.data
