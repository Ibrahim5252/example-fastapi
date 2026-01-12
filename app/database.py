from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#! this block code is for when you use raw SQL rather than SQLalchemy
# while True:
#     try:
#         con = psycopg2.connect(
#             host="localhost",
#             database="Fastapi",
#             user="postgres",
#             password="postgres",
#             cursor_factory=RealDictCursor
#         )
#         cursor = con.cursor()
#         print("Database connection was successful.")
#         break

#     except Exception as error:
#         print("Connection to database failed")
#         print(f"Error: {error}")
#         time.sleep(2)
