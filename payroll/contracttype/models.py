from typing import List, Optional
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from payroll.database.core import Base
from payroll.models import Pagination, PayrollBase, RandomCodeMixin, TimeStampMixin

class TaxPolicy(str, Enum):
    TPolicy1 = "tax_policy_1"
    TPolicy2 = "tax_policy_2"

class InsurancePolicy(str, Enum):
    IPolicy1 = "insurance_policy_1"
    IPolicy2 = "insurance_policy_2"
        
class PayrollContractType(Base, TimeStampMixin, RandomCodeMixin):
    __tablename__ = "contracttypes"
    id: Mapped[int] = mapped_column(primary_key=True)
    explain: Mapped[str] = mapped_column(String(255))
    month: Mapped[int] = mapped_column()
    note: Mapped[Optional[str]] = mapped_column(String(255))
    probation: Mapped[bool] = mapped_column()
    tax_policy: Mapped[TaxPolicy]
    insurance_policy: Mapped[InsurancePolicy]
    
    def __repr__(self) -> str:
        return f"ContractType (name={self.name!r})"

class ContractTypeBase(PayrollBase):
    explain: str
    month: int
    note: Optional[str] = None
    probation: bool
    tax_policy: TaxPolicy
    insurance_policy: InsurancePolicy

class ContractTypeRead(ContractTypeBase):
    id: int
    code: str
    
class ContractTypesRead(PayrollBase):
    data: list[ContractTypeRead] = []

class ContractTypeUpdate(PayrollBase):
    explain: Optional[str] = None
    month: Optional[int] = None
    probation: Optional[bool] = None
    tax_policy: Optional[TaxPolicy] = None
    insurance_policy: Optional[InsurancePolicy] = None

class ContractTypeCreate(ContractTypeBase):
    pass

class ContractTypePagination(Pagination):
    items: List[ContractTypeRead] = []
