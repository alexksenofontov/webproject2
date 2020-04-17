import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Record(SqlAlchemyBase):
    __tablename__ = 'records'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    doc_id = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("doctors.id"), nullable=False)
    people_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("peoples.id"), nullable=True)
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    people = orm.relation('People')
    doctor = orm.relation('Doctor')
