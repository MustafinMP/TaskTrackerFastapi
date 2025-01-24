from datetime import datetime


from sqlalchemy import String, ForeignKey, Table, Column, Integer, TIMESTAMP, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_session import SqlAlchemyBase

user_to_project_model = Table(
    'user_to_project', SqlAlchemyBase.metadata,
    Column('user', Integer, ForeignKey('user.id')),
    Column('project', Integer, ForeignKey('project.id'))
)


class ProjectModel(SqlAlchemyBase):
    __tablename__ = 'project'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    members = relationship('UserModel', secondary=user_to_project_model, back_populates='projects')
    creator = relationship('UserModel', foreign_keys=[creator_id])


class InviteLinkModel(SqlAlchemyBase):
    __tablename__ = 'invite_link'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(nullable=False)
    burn_datetime: Mapped[datetime] = mapped_column(TIMESTAMP)
    key: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
