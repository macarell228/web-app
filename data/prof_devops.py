import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class ProfessionalDevelopment(SqlAlchemyBase):
    __tablename__ = 'professional_development'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    account_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("accounts.id"), nullable=False)
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    during = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
