from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

Base = declarative_base()
engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(bind=engine)

class EmailGeneration(Base):
    __tablename__ = "email_generations"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(256))
    audience = Column(String(256))
    tone = Column(String(64))
    subject = Column(String(512))
    body = Column(Text)
    score = Column(Float)

def init_db():
    Base.metadata.create_all(bind=engine)
