# import pytest
# from datetime import datetime, timedelta

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from fastapi.testclient import TestClient

# from core.settings import app
# from core.env import config
# from core.dependencies.sessions import Base, get_db
  
# engine = create_engine(  
#     config.TEST_DB_URL
# )  


# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()
        

# # @pytest.fixture()
# # def test_db():
# #     Base.metadata.create_all(bind=engine)
# #     yield
# #     Base.metadata.drop_all(bind=engine)
    
# app.dependency_overrides[get_db] = override_get_db
    
# client = TestClient(app)



# def test_create_user():
#     response = client.post(
#         "api/v1/users/",
#         headers={},
#         json={
#             "first_name": "foobar", 
#             "last_name": "FooBar",
#             "email": "GUbar@email.com"
#         },
#     )
#     assert response.status_code == 201
#     assert response.json()['data']['email'] == 'gubar@email.com'
#     assert response.json()['data']['first_name'] == 'foobar'
#     assert response.json()['data']['last_name'] == 'FooBar'


# def test_create_book():
#     response = client.post(
#         "api/v1/books/",
#         headers={},
#         json={
#             "name": "Book 254",
#             "author": "Turn around",
#             "publishers": "Jeremy Trainer",
#         },
#     )
#     assert response.status_code == 201
#     assert response.json()['data']['name'] == 'Book 254'
#     assert response.json()['data']['category'] == 'ACTION'
#     assert response.json()['data']['status'] == 'AVAILABLE'


# def test_create_transaction():
#     response = client.post(
#         "api/v1/users/",
#         headers={},
#         json={
#             "first_name": "foobar", 
#             "last_name": "FooBar",
#             "email": "free@email.com"
#         },
#     )
#     assert response.status_code == 201
#     assert response.json()['data']['email'] == "free@email.com"
#     user_email = response.json()['data']['email']
#     user_id = response.json()['data']['id']
    
    
#     response = client.post(
#         "api/v1/books/",
#         headers={},
#         json={
#             "name": "Rikardo's Vengance",
#             "author": "The Author of 2032",
#             "publishers": "Seven",
#         },
#     )
#     assert response.status_code == 201
#     assert response.json()['data']['name'] == "Rikardo's Vengance"
#     book_name = response.json()['data']['name']
#     book_id = response.json()['data']['id']
    
    
#     response = client.post(
#         "api/v1/transactions/",
#         headers={},
#         json={
#             "book_id": book_id,
#             "book_name": book_name,
#             "user_id": user_id,
#             "user_name": user_email,
#             "status": "BORROWING",
#             "days_till_return": 3
#         },
#     )
    
    
#     assert response.status_code == 201
#     assert response.json()['data']['book_id'] == book_id
#     assert response.json()['data']['user_id'] == user_id
#     assert response.json()['data']['status'] == 'BORROWING'
#     assert response.json()['data']['return_date'] == datetime.now() + timedelta(3)



import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from core.settings import app
from core.env import config
from core.dependencies.sessions import Base, get_db

engine = create_engine('postgresql://cowrywise_frontend_db_user:cUxJVjUAUVb5ouYQ7UaYIkYFpfRdcpYs@dpg-crkndtm8ii6s738397dg-a.oregon-postgres.render.com:5432/test_db')
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    session.begin_nested()  # Create a savepoint
    yield session
    transaction.rollback()
    session.close()
    connection.close()  
    


def test_create_user(db_session):
    response = client.post(
        "api/v1/users/",
        headers={},
        json={
            "first_name": "foobar",
            "last_name": "FooBar",
            "email": "jiji@email.com"
        },
    )
    assert response.status_code == 201
    assert response.json()['data']['email'] == 'jiji@email.com'
    assert response.json()['data']['first_name'] == 'foobar'
    assert response.json()['data']['last_name'] == 'FooBar'


def test_create_book(db_session):
    response = client.post(
        "api/v1/books/",
        headers={},
        json={
            "name": "Book 254",
            "author": "Turn around",
            "publishers": "Jeremy Trainer",
        },
    )
    assert response.status_code == 201
    assert response.json()['data']['name'] == 'Book 254'
    assert response.json()['data']['category'] == 'ACTION'
    assert response.json()['data']['status'] == 'AVAILABLE'


def test_create_transaction(db_session):
    response = client.post(
        "api/v1/users/",
        headers={},
        json={
            "first_name": "foobar",
            "last_name": "FooBar",
            "email": "free@email.com"
        },
    )
    assert response.status_code == 201
    assert response.json()['data']['email'] == "free@email.com"
    user_email = response.json()['data']['email']
    user_id = response.json()['data']['id']
    
    response = client.post(
        "api/v1/books/",
        headers={},
        json={
            "name": "Rikardo's Vengance",
            "author": "The Author of 2032",
            "publishers": "Seven",
        },
    )
    assert response.status_code == 201
    assert response.json()['data']['name'] == "Rikardo's Vengance"
    book_name = response.json()['data']['name']
    book_id = response.json()['data']['id']
    
    response = client.post(
        "api/v1/transactions/",
        headers={},
        json={
            "book_id": book_id,
            "book_name": book_name,
            "user_id": user_id,
            "user_name": user_email,
            "status": "BORROWING",
            "days_till_return": 3
        },
    )
    
    assert response.status_code == 201
    assert response.json()['data']['book_id'] == book_id
    assert response.json()['data']['user_id'] == user_id
    assert response.json()['data']['status'] == 'BORROWING'