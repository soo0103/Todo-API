# FastAPI Todo API

간단한 Todo 리스트 관리용 REST API입니다
FastAPI 프레임워크를 사용하여 학습 및 연습 목적으로 제작했습니다

## Features

- Todo 생성, 조회, 수정, 삭제 (CRUD)
- 검색 및 필터 기능
- 상태 토글 (완료 및 미완료)
- 마감기한, 우선순위 기반 정렬 가능
- Swagger UI 제공 (자동 문서화)

## 프로젝트 구조
```bash
todo-api/
├── crud.py
├── database.py
├── main.py
├── models.py
├── requirements.txt
├── routers
│   └── todo.py
├── sample_data.py
├── schemas.py
└── todos.db
```

## API Endpoints

| 메서드 | 경로                           | 설명                   |
|--------|--------------------------------|------------------------|
| POST   | `/todos/init`                 | 샘플 데이터 초기화     |
| POST   | `/todos`                      | Todo 생성              |
| GET    | `/todos`                      | 모든 Todo 조회         |
| GET    | `/todos/search`              | 키워드 검색            |
| GET    | `/todos/filter`              | 필터링된 Todo 조회     |
| GET    | `/todos/{todo_id}`           | 특정 Todo 조회         |
| PUT    | `/todos/{todo_id}`           | Todo 수정              |
| DELETE | `/todos/{todo_id}`           | Todo 삭제              |
| POST   | `/todos/reset`               | 전체 초기화            |
| PATCH  | `/todos/{todo_id}/toggle`    | 완료 상태 토글         |

- Swagger 문서: [http://localhost:8000/docs](http://localhost:8000/docs)

## 설치 및 실행 방법

```bash
# 1. 가상환경 설정 (선택)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 서버 실행
uvicorn app.main:app --reload
```

## 향후 개선 아이디어
* JWT 기반 사용자 인증 추가  
* 실제 DB 연동
* 통계 기능 (예: 완료율 등)  
* 프론트엔드 연동 (예: React)  
