from uuid import UUID

from app.application.use_cases.record.dtos.get_records_output import GetRecordsOutput
from app.domain.record.record_repository_abstract import RecordRepositoryAbstract
from app.domain.record.services.worked_time_calculator import WorkedTimeCalculator


class GetRecords:
    def __init__(self, worked_time_calculator: WorkedTimeCalculator, record_repository: RecordRepositoryAbstract):
        self.__worked_time_calculator = worked_time_calculator
        self.__record_repository = record_repository

    async def __call__(self, user_id: UUID, ref_month: int, ref_year: int) -> GetRecordsOutput:
        records = await self.__record_repository.list_by_user_month_and_year(
            user_id=user_id, ref_month=ref_month, ref_year=ref_year
        )
        worked_time = self.__worked_time_calculator.get_records_with_missing_clock_outs(records)
        return GetRecordsOutput.to_output(worked_time=worked_time, ref_month=ref_month, ref_year=ref_year)
