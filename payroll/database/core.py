from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from payroll.config import settings

print(settings.SQLALCHEMY_DATABASE_URI)
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
)


class Base(DeclarativeBase):
    pass


def get_db(request: Request):
    return request.state.db


DbSession = Annotated[Session, Depends(get_db)]
