import sqlalchemy
from sqlalchemy import orm

from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Teacher(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'teachers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    account_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("accounts.id"))
    subjects_ids = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    academics = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    dir_of_preparation = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    prof_devop_ids = sqlalchemy.Column(sqlalchemy.Text)
    work_exp = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    account = orm.relation('User')
