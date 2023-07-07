from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud
from . import models
from . import schemas
from .database import SessionLocal, engine


origins = [
    "*",
]
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def Hello():
    return {"Hello": "World!"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def crete_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# Session endpoints
@app.post("/sessions/", response_model=schemas.Session)
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db)):
    db_session = crud.create_session(db=db, session=session)
    if not db_session:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return db_session


@app.post("/sessions/validate/", response_model=schemas.Session)
def validate_session(session: schemas.SessionValidate, db: Session = Depends(get_db)):
    db_session = crud.validate_session(db=db, session=session)
    if not db_session:
        raise HTTPException(status_code=400, detail="Invalid session")
    return db_session


@app.post("/sessions/invalidate/", response_model=schemas.Session)
def invalidate_session(session: schemas.SessionInvalidate, db: Session = Depends(get_db)):
    db_session = crud.invalidate_session(db=db, session=session)
    if not db_session:
        raise HTTPException(status_code=400, detail="Invalid session")
    return db_session


# login page
@app.get("/login/")
def login():
    return {"message": "Login page"}

