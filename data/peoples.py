import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class People(SqlAlchemyBase):
    __tablename__ = 'peoples'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    fname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    birth = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    polis = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.email'),
                              index=True, unique=True, nullable=False)
    user = orm.relation('User')
    record2 = orm.relation('Record', back_populates='people')
