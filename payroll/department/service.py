import logging
from fastapi import HTTPException, status
from payroll.department.models import (
    PayrollDepartment, 
    DepartmentRead,
    DepartmentCreate,
    DepartmentsRead,
    DepartmentUpdate,
)

log = logging.getLogger(__name__)

InvalidCredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=[{"msg": "Could not validate credentials"}],
)

def get_department_by_id(*, db_session, id: int) -> DepartmentRead:
    """Returns a department based on the given id."""
    department = db_session.query(PayrollDepartment).filter(PayrollDepartment.id == id).first()
    return department
    
def get_by_name(*, db_session, name: str) -> DepartmentRead:
    """Returns a department based on the given name."""
    department = db_session.query(PayrollDepartment).filter(PayrollDepartment.name == name).first()
    return department

def get(*, db_session) -> DepartmentsRead:
    """Returns all departments."""
    data = db_session.query(PayrollDepartment).all()
    return DepartmentsRead(data=data)

def get_by_id(*, db_session, id: int) -> DepartmentRead:
    """Returns a department based on the given id."""
    department = get_department_by_id(db_session=db_session, id=id)

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    return department

def create(*, db_session, department_in: DepartmentCreate) -> DepartmentRead:
    """Creates a new department."""
    department = PayrollDepartment(**department_in.model_dump())
    department_db = get_by_name(db_session=db_session, name=department.name)
    if department_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department already exists",
        )
    db_session.add(department)
    db_session.commit()
    return department

def update(*, db_session, id: int, department_in: DepartmentUpdate) -> DepartmentRead:
    """Updates a department with the given data."""
    department_db = get_department_by_id(db_session=db_session, id=id)

    if not department_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
        
    update_data = department_in.model_dump(exclude_unset=True)
    
    existing_department = db_session.query(PayrollDepartment).filter(PayrollDepartment.name == update_data.get('name'), PayrollDepartment.id != id).first()
    
    if existing_department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department name already exists",
        )
    db_session.query(PayrollDepartment).filter(PayrollDepartment.id == id).update(update_data, synchronize_session=False)

    db_session.commit()
    return department_db

def delete(*, db_session, id: int) -> DepartmentRead:
    """Deletes a department based on the given id."""
    query = db_session.query(PayrollDepartment).filter(PayrollDepartment.id == id)
    department = query.first()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
        
    db_session.query(PayrollDepartment).filter(PayrollDepartment.id == id).delete()
    
    db_session.commit()
    return department
