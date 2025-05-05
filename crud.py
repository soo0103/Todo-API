from sqlalchemy.orm import Session
from models import Todo
from schemas import TodoCreate
from datetime import datetime


# 생성
def create_todo(db: Session, todo_data: TodoCreate):
    todo = Todo(
        title=todo_data.title, is_done=todo_data.is_done, created_at=datetime.now()
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


# 읽기 - 하나만
def get_todo_by_id(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()


# 읽기 - 전체
def get_all_todos(db: Session):
    return db.query(Todo).all()


# 수정
def update_todo(db: Session, todo_id: int, todo_data: TodoCreate):
    todo = get_todo_by_id(db, todo_id)
    if not todo:
        return None
    todo.title = todo_data.title
    todo.is_done = todo_data.is_done
    db.commit()
    db.refresh(todo)
    return todo


# 삭제
def delete_todo(db: Session, todo_id: int):
    todo = get_todo_by_id(db, todo_id)
    if not todo:
        return None
    db.delete(todo)
    db.commit()
    return True
