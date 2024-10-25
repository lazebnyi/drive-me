from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    answer_a = Column(String, nullable=False)
    answer_b = Column(String, nullable=False)
    answer_c = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    category = Column(String, nullable=True)  # For specialized questions
