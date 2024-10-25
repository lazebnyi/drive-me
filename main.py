from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Question, Base
from database import engine, get_db
from typing import List
import random

# Initialize the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Question retrieval and quiz management
@app.get("/questions/next")
def get_next_question(current_index: int = 0, db: Session = Depends(get_db)):
    # Retrieve questions categorized by points
    questions_3_points = db.query(Question).filter(Question.points == 3).all()
    questions_2_points = db.query(Question).filter(Question.points == 2).all()
    questions_1_point = db.query(Question).filter(Question.points == 1).all()

    # Retrieve specialized questions
    specialized_questions_3_points = db.query(Question).filter(Question.points == 3, Question.category.isnot(None)).all()
    specialized_questions_2_points = db.query(Question).filter(Question.points == 2, Question.category.isnot(None)).all()
    specialized_questions_1_point = db.query(Question).filter(Question.points == 1, Question.category.isnot(None)).all()

    # Prepare the question list for quiz
    question_pool = (
        random.sample(questions_3_points, min(len(questions_3_points), 1)) +
        random.sample(questions_2_points, min(len(questions_2_points), 1)) +
        random.sample(questions_1_point, min(len(questions_1_point), 1)) +
        random.sample(specialized_questions_3_points, min(len(specialized_questions_3_points), 6)) +
        random.sample(specialized_questions_2_points, min(len(specialized_questions_2_points), 4)) +
        random.sample(specialized_questions_1_point, min(len(specialized_questions_1_point), 2))
    )

    if current_index >= len(question_pool):
        raise HTTPException(status_code=404, detail="No more questions available")

    # Return the next question based on the current index
    return {
        "question": question_pool[current_index].question_text,
        "answers": {
            "A": question_pool[current_index].answer_a,
            "B": question_pool[current_index].answer_b,
            "C": question_pool[current_index].answer_c
        },
        "points": question_pool[current_index].points,
        "index": current_index + 1
    }

# Result calculation (for the final score)
@app.get("/result/{score}")
def get_result(score: int):
    total_possible_points = 74
    passing_score = 3

    if score >= passing_score:
        return {"result": "Passed", "score": score, "total_points": total_possible_points}
    else:
        return {"result": "Failed", "score": score, "total_points": total_possible_points}