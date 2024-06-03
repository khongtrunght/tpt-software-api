from fastapi import APIRouter

from payroll.jobtitle.models import (
    JobTitleRead,
    JobTitleCreate,
    JobTitlesRead,
)
from payroll.database.core import DbSession
from payroll.jobtitle.service import get_by_id, delete, get, create, update

jobtitle_router = APIRouter()

@jobtitle_router.get("/", response_model=JobTitlesRead)
def retrieve_jobtitles(*, db_session: DbSession,):
    return get(db_session=db_session)

@jobtitle_router.get("/{id}", response_model=JobTitleRead)
def retrieve_jobtitle(*, db_session: DbSession, id: int):
    return get_by_id(db_session=db_session, id=id)

@jobtitle_router.post("/", response_model=JobTitleRead)
def create_jobtitle(*, jobtitle_in: JobTitleCreate, db_session: DbSession):
    """Creates a new user."""
    jobtitle = create(db_session=db_session, jobtitle_in=jobtitle_in)
    return jobtitle

@jobtitle_router.put("/{id}", response_model=JobTitleRead)
def update_jobtitle(*, db_session: DbSession, id: int, jobtitle_in: JobTitleCreate):
    return update(db_session=db_session, id=id, jobtitle_in=jobtitle_in)

@jobtitle_router.delete("/{id}", response_model=JobTitleRead)
def delete_jobtitle(*, db_session: DbSession, id: int):
    return delete(db_session=db_session, id=id)
