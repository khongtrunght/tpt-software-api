import logging
from fastapi import HTTPException, status
from payroll.jobtitle.models import (
    PayrollJobTitle, 
    JobTitleRead,
    JobTitleCreate,
    JobTitlesRead,
    JobTitleUpdate,
)

log = logging.getLogger(__name__)

InvalidCredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=[{"msg": "Could not validate credentials"}],
)

def get_jobtitle_by_id(*, db_session, id: int) -> JobTitleRead:
    """Returns a jobtitle based on the given id."""
    jobtitle = db_session.query(PayrollJobTitle).filter(PayrollJobTitle.id == id).first()
    return jobtitle
    
def get_by_name(*, db_session, name: str) -> JobTitleRead:
    """Returns a jobtitle based on the given name."""
    jobtitle = db_session.query(PayrollJobTitle).filter(PayrollJobTitle.name == name).first()
    return jobtitle

def get(*, db_session) -> JobTitlesRead:
    """Returns all jobtitles."""
    data = db_session.query(PayrollJobTitle).all()
    return JobTitlesRead(data=data)

def get_by_id(*, db_session, id: int) -> JobTitleRead:
    """Returns a jobtitle based on the given id."""
    jobtitle = get_jobtitle_by_id(db_session=db_session, id=id)

    if not jobtitle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="JobTitle not found",
        )
    return jobtitle

def create(*, db_session, jobtitle_in: JobTitleCreate) -> JobTitleRead:
    """Creates a new jobtitle."""
    jobtitle = PayrollJobTitle(**jobtitle_in.model_dump())
    jobtitle_db = get_by_name(db_session=db_session, name=jobtitle.name)
    if jobtitle_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="JobTitle already exists",
        )
    db_session.add(jobtitle)
    db_session.commit()
    return jobtitle

def update(*, db_session, id: int, jobtitle_in: JobTitleUpdate) -> JobTitleRead:
    """Updates a jobtitle with the given data."""
    jobtitle_db = get_jobtitle_by_id(db_session=db_session, id=id)

    if not jobtitle_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="JobTitle not found",
        )
        
    update_data = jobtitle_in.model_dump(exclude_unset=True)
    
    existing_jobtitle = db_session.query(PayrollJobTitle).filter(PayrollJobTitle.name == update_data.get('name'), PayrollJobTitle.id != id).first()
    
    if existing_jobtitle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="JobTitle name already exists",
        )
    db_session.query(PayrollJobTitle).filter(PayrollJobTitle.id == id).update(update_data, synchronize_session=False)

    db_session.commit()
    return jobtitle_db

def delete(*, db_session, id: int) -> JobTitleRead:
    """Deletes a jobtitle based on the given id."""
    query = db_session.query(PayrollJobTitle).filter(PayrollJobTitle.id == id)
    jobtitle = query.first()
    
    if not jobtitle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="JobTitle not found",
        )
        
    db_session.query(PayrollJobTitle).filter(PayrollJobTitle.id == id).delete()
    
    db_session.commit()
    return jobtitle
