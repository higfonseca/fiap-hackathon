from datetime import datetime, time, timedelta, timezone

from functional import seq

from app.domain.record.record import Record
from app.domain.record.record_logic import RecordLogic
from app.domain.record.record_type import RecordType


class WorkedTimeCalculator:
    def calculate(self, records: list[Record]) -> dict[datetime, time]:
        grouped_records = seq(records).group_by(lambda record: record.ref_datetime.date()).to_dict()
        worked_times_by_date = {
            ref_date: self.__get_worked_times_by_date(records) for ref_date, records in grouped_records.items()
        }
        return {
            ref_date: self.__get_total_time_within_day(records) for ref_date, records in worked_times_by_date.items()
        }

    def __get_worked_times_by_date(self, records: list[Record]) -> list[datetime]:
        sorted_records = seq(records).sorted(key=lambda record: record.ref_datetime, reverse=True).to_list()
        filled_records = self.__fill_missing_clock_out(sorted_records)
        return [record.ref_datetime for record in filled_records]

    @staticmethod
    def __fill_missing_clock_out(sorted_records: list[Record]) -> list[Record]:
        most_recent_record = sorted_records[0]
        if most_recent_record.type is RecordType.IN:
            default_clock_out = datetime.now(timezone.utc).replace(hour=18, minute=0, second=0, microsecond=0)
            missing_record = RecordLogic.create(
                user=most_recent_record.user, previous_record=most_recent_record, ref_datetime=default_clock_out
            )
            sorted_records.insert(0, missing_record)

        return sorted_records

    def __get_total_time_within_day(self, sorted_times: list[datetime]) -> time:
        pairs = self.__group_times_in_pairs_of_clock_in_clock_out(sorted_times)
        time_deltas = [self.__get_time_delta_from_pair(pair) for pair in pairs]
        time_deltas_sum = sum(time_deltas, timedelta())
        return (datetime.min + time_deltas_sum).time()

    @staticmethod
    def __group_times_in_pairs_of_clock_in_clock_out(sorted_times: list[datetime]) -> set[tuple[datetime, datetime]]:
        it = iter(sorted_times)
        grouped = zip(it, it)
        return set(grouped)

    @staticmethod
    def __get_time_delta_from_pair(pair: tuple[datetime, datetime]) -> timedelta:
        clock_out = pair[0]
        clock_in = pair[1]
        return clock_out - clock_in
