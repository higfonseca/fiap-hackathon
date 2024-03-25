import typing
from datetime import date, datetime, time, timedelta, timezone

from functional import seq

from app.domain.record.enums import RecordType
from app.domain.record.record import Record
from app.domain.record.record_logic import RecordLogic


class WorkedTimeCalculator:
    @staticmethod
    def calculate(records: list[Record]) -> dict[date, time]:
        grouped_sorted_records = WorkedTimeCalculator.get_records_with_missing_clock_outs(records)
        worked_times_by_date = {
            ref_date: WorkedTimeCalculator.__get_worked_times_by_date(records)
            for ref_date, records in grouped_sorted_records.items()
        }
        return {
            ref_date: WorkedTimeCalculator.__get_total_time_within_day(records_datetimes)
            for ref_date, records_datetimes in worked_times_by_date.items()
        }

    @staticmethod
    def get_records_with_missing_clock_outs(records: list[Record]) -> dict[date, list[Record]]:
        grouped_records = seq(records).group_by(lambda record: record.ref_datetime.date()).to_dict()
        return {
            ref_date: WorkedTimeCalculator.__fill_missing_clock_outs(records)
            for ref_date, records in grouped_records.items()
        }

    @staticmethod
    def sum_worked_time(sorted_records: list[Record]) -> time:
        return WorkedTimeCalculator.__get_total_time_within_day([rec.ref_datetime for rec in sorted_records])

    @staticmethod
    def get_time_delta_from_pair(pair: tuple[datetime, datetime]) -> timedelta:
        clock_out = pair[0]
        clock_in = pair[1]
        return clock_out - clock_in

    @staticmethod
    def __fill_missing_clock_outs(daily_records: list[Record]) -> list[Record]:
        sorted_records = seq(daily_records).sorted(lambda record: record.ref_datetime, reverse=True).to_list()
        most_recent_record = sorted_records[0]
        if most_recent_record.type is RecordType.IN:
            default_clock_out = datetime.now(timezone.utc).replace(hour=18, minute=0, second=0, microsecond=0)
            missing_record = RecordLogic.create(
                user=most_recent_record.user, todays_previous_record=most_recent_record, ref_datetime=default_clock_out
            )
            daily_records.insert(0, missing_record)

        result = seq(daily_records).sorted(lambda record: record.ref_datetime, reverse=True).to_list()
        return typing.cast(list[Record], result)

    @staticmethod
    def __get_worked_times_by_date(sorted_records: list[Record]) -> list[datetime]:
        return [record.ref_datetime for record in sorted_records]

    @staticmethod
    def __get_total_time_within_day(sorted_times: list[datetime]) -> time:
        pairs = WorkedTimeCalculator.__group_times_in_pairs_of_clock_in_clock_out(sorted_times)
        time_deltas = [WorkedTimeCalculator.get_time_delta_from_pair(pair) for pair in pairs]
        time_deltas_sum = sum(time_deltas, timedelta())
        return (datetime.min + time_deltas_sum).time()

    @staticmethod
    def __group_times_in_pairs_of_clock_in_clock_out(sorted_times: list[datetime]) -> set[tuple[datetime, datetime]]:
        it = iter(sorted_times)
        grouped = zip(it, it)
        return set(grouped)
