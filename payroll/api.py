from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from payroll.auth.service import get_current_user
from payroll.auth.views import user_router, auth_router
from payroll.department.views import department_router
from payroll.jobtitle.views import jobtitle_router
from payroll.contracttype.views import contracttype_router

# WARNING: Don't use this unless you want unauthenticated routes
authenticated_api_router = APIRouter()


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
authenticated_api_router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(department_router, prefix="/departments", tags=["departments"])
router.include_router(jobtitle_router, prefix="/jobtitles", tags=["jobtitles"])
router.include_router(contracttype_router, prefix="/contracttypes", tags=["contracttypes"])

api_router.include_router(
    authenticated_api_router,
    dependencies=[Depends(get_current_user)],
)
