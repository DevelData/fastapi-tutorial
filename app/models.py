from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP
from app.database import Base



class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="true", nullable=False)
    #created_at = Column(TIMESTAMP, nullable=False)