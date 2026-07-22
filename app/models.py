from app.database import Base
from sqlalchemy import Integer, String, Column

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=False)
    url = Column(String, nullable=False)
    keyword = Column(String, nullable=False)
    source = Column(String, nullable=False)
    telegram_id = Column(String, nullable=True)