from sqlalchemy.orm import Session
from models import Todo as TodoModel
from datetime import datetime

def create_sample_todos(db: Session):
    sample_todos = [
        TodoModel(title="FastAPI 공부하기", is_done=False, created_at=datetime.utcnow()),
        TodoModel(title="운동 30분 하기", is_done=True, created_at=datetime.utcnow()),
        TodoModel(title="책 10페이지 읽기", is_done=False, created_at=datetime.utcnow()),
        TodoModel(title="친구에게 연락하기", is_done=False, created_at=datetime.utcnow()),
        TodoModel(title="커피 마시면서 산책", is_done=True, created_at=datetime.utcnow()),
    ]
    
    db.add_all(sample_todos)
    db.commit()
    return sample_todos