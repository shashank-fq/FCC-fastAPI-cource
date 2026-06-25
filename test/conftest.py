# any file in the parenty directory of this file will have access to this file by default no need of import all scope modules functions this is made so that all files like test_users, test_votes and test_posts all have access to this file


from fastapi.testclient import TestClient
from app.main import app
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models
# from alembic import command

SQLALCHIME_DATABSE_URL = 'postgresql://postgres:dhisdat@localhost:5432/test_fastapi'


# SQLALCHIME_DATABSE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/test_{settings.database_name}"

engine = create_engine(SQLALCHIME_DATABSE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)

# Base = declarative_base()

# def override_get_db():
#     db = TestingSessionLocal()

#     try:
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# client = TestClient(app)
@pytest.fixture()
def client(session):
    # # when test finises the tables are droped
    # # for new test new tables are created(old)

    # #now if error occurs we can see db 
    # Base.metadata.drop_all(bind=engine)

    # run our code before we run our test
    # Base.metadata.create_all(bind=engine)//moved to session

    # command.upgrade("head")

    # yield TestClient(app)

    # command.downgrade("base")
    # run our code after our test finishes



    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}
    res =client.post("/users/", json= user_data)
    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello1234@gmail.com", "password": "password1234"}
    res =client.post("/users/", json= user_data)
    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client



@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "1st title",
        "content": "1st content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },{
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_user2['id']
    }]
    def create_post_model(post):
        return models.Post(**post)
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    # session.add_all([models.Post(title = "1st user", content = "1st content", owner_id = test_user['id']),
    #                  models.Post(title = "2nd user", content = "2nd content", owner_id = test_user['id']),
    #                  models.Post(title = "3rd user", content = "3rd content", owner_id = test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts