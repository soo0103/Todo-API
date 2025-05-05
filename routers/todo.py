from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import asc, desc, nulls_last
from datetime import datetime, timedelta, date

from database import get_db
from models import Todo as TodoModel
from schemas import Todo, TodoCreate, TodoUpdate

from models import Base
from database import engine

router = APIRouter(prefix="/todos", tags=["Todos"])


# 샘플 데이터 생성
@router.post("/init")
def init_sample_data(db: Session = Depends(get_db)):

    now = datetime.utcnow().replace(microsecond=0)

    sample_todos = [
    TodoModel(title="아침 운동하기", is_done=True, priority="high", due_date=now + timedelta(hours=6)),
    TodoModel(title="개발 공부 2시간", is_done=False, priority="medium", due_date=now + timedelta(days=1)),
    TodoModel(title="점심 약속", is_done=True, priority="low", due_date=now - timedelta(days=1)),
    TodoModel(title="책 1장 읽기", is_done=False, priority="medium", due_date=now + timedelta(days=2)),
    TodoModel(title="강아지 산책", is_done=False, priority="low", due_date=now + timedelta(hours=12)),
    TodoModel(title="친구에게 연락하기", is_done=False, priority="high", due_date=now + timedelta(days=3)),
    TodoModel(title="뭐 먹을지 고민하기", is_done=False, priority="medium", due_date=now + timedelta(days=1, hours=2)),
    TodoModel(title="벚꽃 보러가기", is_done=True, priority="high", due_date=now - timedelta(days=2)),
    TodoModel(title="다음 약속 날짜 정하기", is_done=False, priority="low", due_date=now + timedelta(days=4)),
    TodoModel(title="지금 당장 놀기", is_done=False, priority="medium"),
    ]
    db.add_all(sample_todos)
    db.commit()
    return {"message": "Todo init complete!"}


# 생성
@router.post("", response_model=Todo)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoModel(title=todo.title, priority=todo.priority)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# 검색
@router.get("/search", response_model=List[Todo])
def search_todos(query: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todos = (
        db.query(TodoModel)
        .filter(TodoModel.title.ilike(f"%{query}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )

    if not todos:
        raise HTTPException(status_code=404, detail="No todos found matching the query")

    return todos


# 필터
@router.get("/filter", response_model=List[Todo])
def filter_todos(is_done: bool, db: Session = Depends(get_db)):
    return db.query(TodoModel).filter(TodoModel.is_done == is_done).all()


# 조회
@router.get("", response_model=List[Todo])
def read_all_todos(
    skip: int = 0,
    limit: int = 20,
    sort_by: str = Query("created_at", enum=["created_at", "priority", "title", "due_date"]),
    order: str = Query("asc", enum=["asc", "desc"]),
    priority: Optional[str] = Query(None, enum=["low", "medium", "high"]),
    completed: Optional[bool] = Query(None),
    today: Optional[bool] = Query(False),
    due_from: Optional[date] = Query(None),
    due_to: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(TodoModel)

    if priority:
        query = query.filter(TodoModel.priority == priority)
    if completed is not None:
        query = query.filter(TodoModel.is_done == completed)
    if today:
        today_date = date.today()
        query = query.filter(TodoModel.due_date == today_date)
    if due_from:
        query = query.filter(TodoModel.due_date >= due_from)
    if due_to:
        query = query.filter(TodoModel.due_date <= due_to)

    if sort_by == "priority":
        priority_order = {
            "low": 0,
            "medium": 1,
            "high": 2
        }
        todos = sorted(query.all(), key=lambda todo: priority_order[todo.priority], reverse=(order == "desc"))
        return todos[skip: skip + limit]

    if sort_by == "due_date":
        sort_column = getattr(TodoModel, "due_date")
        sort_column = nulls_last(desc(sort_column)) if order == "desc" else nulls_last(asc(sort_column))
    else:
        sort_column = getattr(TodoModel, sort_by)
        sort_column = sort_column.desc() if order == "desc" else sort_column.asc()

    todos = query.order_by(sort_column).offset(skip).limit(limit).all()
    return todos


# 조회 - 단일
@router.get("/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# 수정
@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = updated.title
    todo.is_done = updated.is_done
    todo.priority = updated.priority
    db.commit()
    db.refresh(todo)
    return todo


# 삭제
@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": f"Todo {todo_id} deleted successfully"}


# 초기화
@router.post("/reset")
def reset_todos():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"message": "Todos reset complete."}


# 토글
@router.patch("/{todo_id}/toggle", response_model=Todo)
def toggle_todo_status(
    todo_id: int = Path(..., description="The ID of the todo to toggle"),
    db: Session = Depends(get_db)
):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.is_done = not todo.is_done
    db.commit()
    db.refresh(todo)

    return todo