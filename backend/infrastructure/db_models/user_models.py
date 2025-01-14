from datetime import datetime
from typing import Optional

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(SqlAlchemyBase, SerializerMixin):
    """Main user model.

    :param id: the unique user identification key.
    :param name: just the username.
    :param email: the email of the user.
    :param hashed_password: the hash of user password.
    :param created_date: the date, when ...
    :param image: the filename of user profile image.
    """

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]] = mapped_column(String)
    email: Mapped[Optional[str]] = mapped_column(String, index=True, unique=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    image: Mapped[Optional[str]] = mapped_column(String, default='default.png')

    projects = relationship('ProjectModel', secondary='user_to_project', back_populates='members')

    oauth_yandex_id: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
