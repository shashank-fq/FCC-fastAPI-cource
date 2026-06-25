# from fastapi.testclient import TestClient
# from app.main import app
# import pytest

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from app.config import settings
# from app.database import get_db
# from app.database import Base
# # from alembic import command

# SQLALCHIME_DATABSE_URL = 'postgresql://postgres:dhisdat@localhost:5432/test_fastapi'


# # SQLALCHIME_DATABSE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/test_{settings.database_name}"

# engine = create_engine(SQLALCHIME_DATABSE_URL)

# TestingSessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )

# Base.metadata.create_all(bind=engine)

# # Base = declarative_base()

# # def override_get_db():
# #     db = TestingSessionLocal()

# #     try:
# #         yield db
# #     finally:
# #         db.close()


# # app.dependency_overrides[get_db] = override_get_db

# @pytest.fixture()
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()

#     try:
#         yield db
#     finally:
#         db.close()


# # client = TestClient(app)
# @pytest.fixture()
# def client(session):
#     # # when test finises the tables are droped
#     # # for new test new tables are created(old)

#     # #now if error occurs we can see db 
#     # Base.metadata.drop_all(bind=engine)

#     # run our code before we run our test
#     # Base.metadata.create_all(bind=engine)//moved to session

#     # command.upgrade("head")

#     # yield TestClient(app)

#     # command.downgrade("base")
#     # run our code after our test finishes



#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)