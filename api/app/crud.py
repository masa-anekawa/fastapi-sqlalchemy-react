from uuid import uuid4 as UUID
from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Create, validate, and invalidate sessions
def create_session(db: Session, session: schemas.SessionCreate):
    # try getting user and validating password
    db_user = db.query(models.User).filter(models.User.id == session.user_id).first()
    if not db_user:
        return None
    if not db_user.hashed_password == session.password + "notreallyhashed":
        return None

    # create session
    session_id = UUID()
    db_session = models.Session(
        user_id=session.user_id,
        session_id=str(session_id),
        is_active=True,
        expires_at="2024-01-01T00:00:00",
        )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def validate_session(db: Session, session: schemas.SessionValidate):
    # Check if valid session exists for given user id, before given expired_at period, and is active
    db_session = db.query(models.Session).filter(
        models.Session.user_id == session.user_id,
        models.Session.session_id == session.session_id,
        models.Session.is_active,
        models.Session.expires_at > "2021-01-01T00:00:00",
        ).first()
    if not db_session:
        return None
    return db_session


def invalidate_session(db: Session, session: schemas.SessionInvalidate):
    # invalidate existing session for given user id and session id, then return invalidated session
    db_session = db.query(models.Session).filter(
        models.Session.user_id == session.user_id,
        models.Session.session_id == session.session_id,
        ).first()
    if not db_session:
        return None
    db_session.is_active = False
    db.commit()
    db.refresh(db_session)
    return db_session
