from __future__ import annotations

from datetime import date, time

from functional import seq
from pydantic import BaseModel

from app.domain.record.record import Record
from app.domain.record.services.worked_time_calculator import WorkedTimeCalculator


class GetRecordsTimesOutput(BaseModel):  # type:ignore[misc]
    clock_in: time
    clock_out: time


class GetRecordsSummaryOutput(BaseModel):  # type:ignore[misc]
    date: date
    worked_time: time
    times: list[GetRecordsTimesOutput]


class GetRecordsOutput(BaseModel):  # type:ignore[misc]
    records: list[GetRecordsSummaryOutput]
    ref_month: int
    ref_year: int

    @staticmethod
    def to_output(worked_time: dict[date, list[Record]], ref_month: int, ref_year: int) -> GetRecordsOutput:
        return GetRecordsOutput(
            records=[
                GetRecordsSummaryOutput(
                    date=ref_date,
                    worked_time=WorkedTimeCalculator.sum_worked_time(records),
                    times=GetRecordsOutput.__get_times(records),
                )
                for ref_date, records in worked_time.items()
            ],
            ref_month=ref_month,
            ref_year=ref_year,
        )

    @staticmethod
    def __get_times(records: list[Record]) -> list[GetRecordsTimesOutput]:
        times = [record.ref_datetime.time() for record in records]
        it = iter(times)
        grouped = zip(it, it)
        pairs = set(grouped)
        ordered_pairs = seq(pairs).order_by(lambda pair: pair[0]).to_list()

        return [
            GetRecordsTimesOutput(
                clock_in=pair[1],
                clock_out=pair[0],
            )
            for pair in ordered_pairs
        ]
