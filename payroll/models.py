from datetime import datetime, timezone
import random
import string


from pydantic import BaseModel
from pydantic.types import conint, constr, SecretStr
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declared_attr
# pydantic type that limits the range of primary keys
PrimaryKey = conint(gt=0, lt=2147483647)
NameStr = constr(pattern=r"^(?!\s*$).+", strip_whitespace=True, min_length=3)
CompanySlug = constr(pattern=r"^[\w]+(?:_[\w]+)*$", min_length=3)


# SQLAlchemy models...
class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    # updated_at = Column(
    #     DateTime,
    #     default=datetime.now(timezone.utc),
    #     onupdate=datetime.now(timezone.utc),
    # )
    
class RandomCodeMixin:
    @staticmethod
    def generate_random_code(length=8):
        """Generates a random alphanumeric code of specified length."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    @declared_attr
    def code(cls):
        return Column(String(20), unique=True, nullable=False, default=lambda: cls.generate_random_code())

    @classmethod
    def generate_and_set_code(cls, target, value, oldvalue, initiator):
        """Generates and sets a random code if not already set."""
        if not value:
            target.code = cls.generate_random_code()

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
