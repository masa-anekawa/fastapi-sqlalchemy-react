from typing_extensions import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base


pk_id = Annotated[int, mapped_column(primary_key=True, index=True)]
email = Annotated[str, mapped_column(unique=True, index=True)]
fk_user_id = Annotated[int, mapped_column(ForeignKey("users.id"))]
str_indexed = Annotated[str, mapped_column(index=True)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[pk_id] = mapped_column(init=False)
    email: Mapped[email]
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    items: Mapped[list["Item"]] = relationship(back_populates="owner", default_factory=list)
    sessions: Mapped[list["Session"]] = relationship(back_populates="user", default_factory=list)


class Item(Base):
    __tablename__ = "items"

    id: Mapped[pk_id] = mapped_column(init=False)
    title: Mapped[str]
    description: Mapped[str]
    owner_id: Mapped[fk_user_id]

    owner: Mapped["User"] = relationship(back_populates="items", default=None)


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[pk_id] = mapped_column(init=False)
    session_id: Mapped[str_indexed]
    user_id: Mapped[fk_user_id]
    is_active: Mapped[bool] = mapped_column(default=True)
    expires_at: Mapped[str] = mapped_column(default="2024-01-01T00:00:00")

    user: Mapped["User"] = relationship(back_populates="sessions", default=None)
