from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Not used because all db queries use SQLAlchemy instead
# import psycopg2
# from psycopg2.extras import RealDictCursor
# This caused a bug - changing to the correct password did not establish
# normal flow.
# while True: 
# try:
#     conn = psycopg2.connect(
#         host="localhost",
#         database="fastapi",
#         user="postgres",
#         password="password",
#         cursor_factory=RealDictCursor
#         )
#     cursor = conn.cursor()
#     print("Connection to database was successful!")
#     #break
# except Exception as err:
#     print(f"Connection attempt to database failed. Error: {err}")
#     #time.sleep(1.5)