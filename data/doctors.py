import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Doctor(SqlAlchemyBase):
    __tablename__ = 'doctors'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    fname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    profile = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.email"),
                              index=True, unique=True, nullable=False)

    user = orm.relation('User')
    record = orm.relation('Record', back_populates='doctor')
