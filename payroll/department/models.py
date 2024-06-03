from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from payroll.database.core import Base
from payroll.models import Pagination, PayrollBase, RandomCodeMixin, TimeStampMixin


class PayrollDepartment(Base, TimeStampMixin, RandomCodeMixin):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    
    def __repr__(self) -> str:
        return f"Department (name={self.name!r})"

class DepartmentBase(PayrollBase):
    name: str
    description: Optional[str] = None

class DepartmentRead(DepartmentBase):
    id: int
    code: str
    
class DepartmentsRead(PayrollBase):
    data: list[DepartmentRead] = []
    # count: int

class DepartmentUpdate(PayrollBase):
    name: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentPagination(Pagination):
    items: List[DepartmentRead] = []
