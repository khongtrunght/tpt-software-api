from datetime import datetime, timezone


from pydantic import BaseModel
from pydantic.types import conint, constr, SecretStr
from sqlalchemy import Column, DateTime

# pydantic type that limits the range of primary keys
PrimaryKey = conint(gt=0, lt=2147483647)
NameStr = constr(pattern=r"^(?!\s*$).+", strip_whitespace=True, min_length=3)
CompanySlug = constr(pattern=r"^[\w]+(?:_[\w]+)*$", min_length=3)


# SQLAlchemy models...
class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )


# Pydantic models...
class PayrollBase(BaseModel):
    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        str_strip_whitespace = True

        json_encoders = {
            # custom output conversion for datetime
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ") if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }


class Pagination(PayrollBase):
    itemsPerPage: int
    page: int
    total: int
