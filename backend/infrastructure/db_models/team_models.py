from datetime import datetime


from sqlalchemy import String, ForeignKey, Table, Column, Integer, TIMESTAMP, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase

user_to_team = Table(
    'user_to_team', SqlAlchemyBase.metadata,
    Column('user', Integer, ForeignKey('user.id')),
    Column('team', Integer, ForeignKey('team.id'))
)


class TeamModel(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'team'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    members = relationship('UserModel', secondary=user_to_team, back_populates='teams')
    creator = relationship('UserModel', foreign_keys=[creator_id])


class InviteLinkModel(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'invite_link'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(nullable=False)
    burn_datetime: Mapped[datetime] = mapped_column(TIMESTAMP)
    key: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
