from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.application.dtos.token import Token
from app.application.use_cases.user.authenticate_user import AuthenticateUser
from app.infrastructure.container import ApplicationContainer
from app.presentation.helpers.custom_router import APICustomRouter

router = APICustomRouter(prefix="/authenticate")


@router.post("", status_code=status.HTTP_200_OK)
@inject
async def authenticate(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    use_case: AuthenticateUser = Depends(Provide[ApplicationContainer.authenticate_user]),
) -> Token:
    return await use_case(identifier=form_data.username, password=form_data.password)
