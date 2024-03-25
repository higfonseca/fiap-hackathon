from enum import Enum


class RecordType(Enum):
    IN = "in"
    OUT = "out"


class EventType(Enum):
    WORK = "work"
    INTERVAL = "interval"
