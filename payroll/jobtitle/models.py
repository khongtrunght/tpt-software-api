from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from payroll.database.core import Base
from payroll.models import Pagination, PayrollBase, RandomCodeMixin, TimeStampMixin


class PayrollJobTitle(Base, TimeStampMixin, RandomCodeMixin):
    __tablename__ = "jobtitles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    
    def __repr__(self) -> str:
        return f"JobTitle (name={self.name!r})"

class JobTitleBase(PayrollBase):
    name: str
    description: Optional[str] = None

class JobTitleRead(JobTitleBase):
    id: int
    code: str
    
class JobTitlesRead(PayrollBase):
    data: list[JobTitleRead] = []
    # count: int

class JobTitleUpdate(PayrollBase):
    name: Optional[str] = None

class JobTitleCreate(JobTitleBase):
    pass

class JobTitlePagination(Pagination):
    items: List[JobTitleRead] = []
