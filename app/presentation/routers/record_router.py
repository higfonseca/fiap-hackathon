from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Query
from starlette import status

from app.application.use_cases.record.create_record import CreateRecord
from app.application.use_cases.record.dtos.get_records_output import GetRecordsOutput
from app.application.use_cases.record.get_records import GetRecords
from app.infrastructure.container import ApplicationContainer
from app.presentation.helpers.authentication_helper import AuthenticationHelper
from app.presentation.helpers.custom_router import APICustomRouter

router = APICustomRouter(prefix="/records")


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_record(
    user_id: Annotated[UUID, Depends(AuthenticationHelper.get_current_user_id)],
    use_case: CreateRecord = Depends(Provide[ApplicationContainer.create_record]),
) -> None:
    await use_case(user_id=user_id)


@router.get("", status_code=status.HTTP_200_OK)
@inject
async def get_records(
    user_id: Annotated[UUID, Depends(AuthenticationHelper.get_current_user_id)],
    ref_month: int = Query(...),
    ref_year: int = Query(...),
    use_case: GetRecords = Depends(Provide[ApplicationContainer.get_records]),
) -> GetRecordsOutput:
    return await use_case(user_id=user_id, ref_month=ref_month, ref_year=ref_year)
