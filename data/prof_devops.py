import sqlalchemy
from sqlalchemy import orm

from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class ProfessionalDevelopment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'professional_development'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    account_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.account_id"), nullable=False)
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    during = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    teacher = orm.relation('Teacher')
