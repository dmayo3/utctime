from __future__ import annotations
from datetime import datetime, timezone, timedelta
from typing import Union


# Note that datetime.UTC wasn't added until python 3.11
UTC = timezone.utc


BASE_FMT = "%Y-%m-%dT%H:%M:%S"


# Output formats
ISO_8601_FORMAT_MS = f"{BASE_FMT}.%fZ"
ISO_8601_FORMAT = f"{BASE_FMT}Z"


# All combinations of: [with/without microseconds] x [Z or +HH:MM timezone]
PARSE_FORMATS = [
    ISO_8601_FORMAT_MS,
    ISO_8601_FORMAT,
    f"{BASE_FMT}.%f%z",
    f"{BASE_FMT}%z",
]


OptInt = Union[int, None]


class UtcTime:
    def __init__(
        self,
        year: int,
        month: int = 1,
        day: int = 1,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ):
        self._dt = datetime(
            year, month, day, hour, minute, second, microsecond, tzinfo=UTC
        )

    @staticmethod
    def copy_from(other: datetime | UtcTime) -> UtcTime:
        dtime = _unwrap(other)
        return _from_datetime(dtime)

    @staticmethod
    def now() -> UtcTime:
        return _from_datetime(datetime.now(UTC))

    @staticmethod
    def parse_iso(iso8601: str) -> UtcTime:
        for fmt in PARSE_FORMATS:
            try:
                return _from_datetime(datetime.strptime(iso8601, fmt).astimezone(UTC))
            except ValueError:
                pass
        raise ValueError(
            f"time data {iso8601} does not match timezoned ISO 8601 "
            "datetime format: %Y-%m-%dT%H:%M:%S[.%f][%z|Z]"
        )

    @property
    def year(self):
        return self._dt.year

    @property
    def month(self):
        return self._dt.month

    @property
    def day(self):
        return self._dt.day

    @property
    def hour(self):
        return self._dt.hour

    @property
    def minute(self):
        return self._dt.minute

    @property
    def second(self):
        return self._dt.second

    @property
    def microsecond(self):
        return self._dt.microsecond

    def todatetime(self) -> datetime:
        return self._dt

    def replace(
        self,
        year: OptInt = None,
        month: OptInt = None,
        day: OptInt = None,
        hour: OptInt = None,
        minute: OptInt = None,
        second: OptInt = None,
        microsecond: OptInt = None,
    ) -> UtcTime:
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        if hour is None:
            hour = self.hour
        if minute is None:
            minute = self.minute
        if second is None:
            second = self.second
        if microsecond is None:
            microsecond = self.microsecond

        return _from_datetime(
            self.todatetime().replace(
                year, month, day, hour, minute, second, microsecond
            )
        )

    def iso(self) -> str:
        if self.todatetime().microsecond:
            return self.todatetime().strftime(ISO_8601_FORMAT_MS)

        return self.todatetime().strftime(ISO_8601_FORMAT)

    def timestamp(self) -> float:
        return self.todatetime().timestamp()

    def __repr__(self) -> str:
        return f"UtcTime({self.iso()})"

    def __add__(self, other) -> UtcTime:
        if isinstance(other, timedelta):
            return _from_datetime(self.todatetime() + other)

        raise TypeError(f"Not a timedelta object: {other}")

    def __sub__(self, other) -> UtcTime:
        if isinstance(other, timedelta):
            return _from_datetime(self.todatetime() - other)

        raise TypeError(f"Not a timedelta object: {other}")

    def __lt__(self, other) -> bool:
        return self.todatetime() < _unwrap(other)

    def __le__(self, other) -> bool:
        return self.todatetime() <= _unwrap(other)

    def __eq__(self, other) -> bool:
        return self.todatetime() == _unwrap(other)

    def __ge__(self, other) -> bool:
        return self.todatetime() >= _unwrap(other)

    def __gt__(self, other) -> bool:
        return self.todatetime() > _unwrap(other)


def _from_datetime(dtime: datetime) -> UtcTime:
    if dtime.tzinfo != UTC:
        raise ValueError(f"{dtime} does not have a UTC timezone")

    return UtcTime(
        dtime.year,
        dtime.month,
        dtime.day,
        dtime.hour,
        dtime.minute,
        dtime.second,
        dtime.microsecond,
    )


def _unwrap(other) -> datetime:
    if isinstance(other, UtcTime):
        return other.todatetime()

    if isinstance(other, datetime):
        return other

    raise TypeError(
        f"Can't compare with {other} as it's not a UtcTime or datetime object"
    )
