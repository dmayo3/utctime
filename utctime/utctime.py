from __future__ import annotations
from datetime import datetime, timezone, timedelta
from typing import Optional, Any


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


class UtcTime:
    """
    Wrapper class for :py:class:`datetime.datetime` that's always in UTC.

    It behaves in a similar manner and with similar conventions.

    You can use it as a type, use the constructor, or use one of the static
    methods to create :class:`utctime.UtcTime` instances.
    """

    # pylint: disable=too-many-positional-arguments
    def __init__(
        self: UtcTime,
        year: int,
        month: int = 1,
        day: int = 1,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ):
        """
        Construct new :class:`utctime.UtcTime` with a given date/time.

        All fields but year are optional.

        Unlike the :py:class:`datetime.datetime` constructor, the
        :py:attr:`datetime.datetime.tzinfo` argument may not be specified.
        """
        self._dt = datetime(
            year,
            month,
            day,
            hour,
            minute,
            second,
            microsecond,
            tzinfo=UTC,
        )

    @staticmethod
    def copy_from(other: datetime | UtcTime) -> UtcTime:
        """
        Return a :class:`utctime.UtcTime` from another
        :class:`utctime.UtcTime` or UTC :py:class:`datetime.datetime` object.
        """
        dtime = _unwrap(other)
        return _from_datetime(dtime)

    @staticmethod
    def now() -> UtcTime:
        """
        Current UTC date and time.

        Unlike :py:func:`datetime.now`, :py:attr:`datetime.datetime.tzinfo` may not be specified.
        """
        return _from_datetime(datetime.now(UTC))

    @staticmethod
    def parse_iso(iso8601: str) -> UtcTime:
        """
        Parse an ISO 8601 date-time string and returns a :class:`utctime.UtcTime` instance.

        The string must include timezone information (Z or +HH:MM offset).

        The string may include microseconds.

        The exact format accepted is: `%Y-%m-%dT%H:%M:%S[.%f][%z|Z]`.
        """
        for fmt in PARSE_FORMATS:
            try:
                return _from_datetime(datetime.strptime(iso8601, fmt).astimezone(UTC))
            except ValueError:
                pass
        raise ValueError(
            f"time data {iso8601} does not match timezoned ISO 8601 "
            "datetime format: %Y-%m-%dT%H:%M:%S[.%f][%z|Z]",
        )

    @property
    def year(self: UtcTime) -> int:
        """1 - 9999 as per :py:attr:`datetime.datetime.year`"""
        return self._dt.year

    @property
    def month(self: UtcTime) -> int:
        """1 - 12 as per :py:attr:`datetime.datetime.month`"""
        return self._dt.month

    @property
    def day(self: UtcTime) -> int:
        """
        1 - 31 (depending on the month) as per :py:attr:`datetime.datetime.day`
        """
        return self._dt.day

    @property
    def hour(self: UtcTime) -> int:
        """0 - 23 as per :py:attr:`datetime.datetime.hour`"""
        return self._dt.hour

    @property
    def minute(self: UtcTime) -> int:
        """0 - 59 as per :py:attr:`datetime.datetime.minute`"""
        return self._dt.minute

    @property
    def second(self: UtcTime) -> int:
        """0 - 59 as per :py:attr:`datetime.datetime.second`"""
        return self._dt.second

    @property
    def microsecond(self: UtcTime) -> int:
        """0 - 999999 as per :py:attr:`datetime.datetime.microsecond`"""
        return self._dt.microsecond

    def todatetime(self: UtcTime) -> datetime:
        """Converts back to a regular :py:class:`datetime.datetime` with a UTC timezone."""
        return self._dt

    # pylint: disable=too-many-positional-arguments
    def replace(
        self: UtcTime,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
        microsecond: Optional[int] = None,
    ) -> UtcTime:
        """
        Replace any of the date/time fields.

        Unlike :py:meth:`datetime.replace` it does not allow replacing
        :py:attr:`datetime.datetime.tzinfo` or :py:attr:`datetime.fold`.

        Returns a new :class:`utctime.UtcTime`.
        """
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
                year,
                month,
                day,
                hour,
                minute,
                second,
                microsecond,
            ),
        )

    def iso(self: UtcTime) -> str:
        """
        Returns an ISO 8601 formatted date-time string.

        Microseconds are included if they are non-zero.

        The timezone specifier is always Z.
        """
        if self.todatetime().microsecond:
            return self.todatetime().strftime(ISO_8601_FORMAT_MS)

        return self.todatetime().strftime(ISO_8601_FORMAT)

    def timestamp(self: UtcTime) -> float:
        """
        Seconds since the epoch (1970) as a float, as per
        :py:meth:`datetime.datetime.timestamp`.
        """
        return self.todatetime().timestamp()

    def __repr__(self: UtcTime) -> str:
        return f"UtcTime({self.iso()})"

    def __add__(self: UtcTime, other: Any) -> UtcTime:
        """Add a ``timedelta`` and return a new :class:`utctime.UtcTime`."""
        if isinstance(other, timedelta):
            return _from_datetime(self.todatetime() + other)

        raise TypeError(f"Not a timedelta object: {other}")

    def __sub__(self: UtcTime, other: Any) -> UtcTime:
        """Subtract a :py:class:`datetime.timedelta` and return a new :class:`utctime.UtcTime`."""
        if isinstance(other, timedelta):
            return _from_datetime(self.todatetime() - other)

        raise TypeError(f"Not a timedelta object: {other}")

    def __lt__(self: UtcTime, other: Any) -> bool:
        """
        Return `True` if `other` is a :class:`datetime.datetime` or :class:`utctime.UtcTime`
        that comes before before this :class:`utctime.UtcTime` instance, otherwise
        `False`.

        This cannot be compared with naive datetimes that lack a timezone.
        """
        return self.todatetime() < _unwrap(other)

    def __le__(self: UtcTime, other: Any) -> bool:
        """
        Return `True` if `other` is a :class:`datetime.datetime` or :class:`utctime.UtcTime`
        that comes before before or at the same time as this :class:`utctime.UtcTime`
        instance, otherwise `False`.

        This cannot be compared with naive datetimes that lack a timezone.
        """
        return self.todatetime() <= _unwrap(other)

    def __eq__(self: UtcTime, other: Any) -> bool:
        """
        Return `True` if `other` is a :class:`datetime.datetime` or :class:`utctime.UtcTime`
        that is at the same time as this :class:`utctime.UtcTime` instance,
        otherwise `False`.

        Naive datetimes without a timezone are never equal to
        this :class:`utctime.UtcTime` instance.
        """
        return self.todatetime() == _unwrap(other)

    def __ge__(self: UtcTime, other: Any) -> bool:
        """
        Return `True` if `other` is a :class:`datetime.datetime` or :class:`utctime.UtcTime`
        that comes before after or at the same time as this :class:`utctime.UtcTime`
        instance, otherwise `False`.

        This cannot be compared with naive datetimes that lack a timezone.
        """
        return self.todatetime() >= _unwrap(other)

    def __gt__(self: UtcTime, other: Any) -> bool:
        """
        Return `True` if `other` is a :class:`datetime.datetime` or :class:`utctime.UtcTime`
        that comes before after this :class:`utctime.UtcTime` instance, otherwise `False`.

        This cannot be compared with naive datetimes that lack a timezone.
        """
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


def _unwrap(other: Any) -> datetime:
    if isinstance(other, UtcTime):
        return other.todatetime()

    if isinstance(other, datetime):
        return other

    raise TypeError(
        f"Can't compare with '{other}' as it's not a UtcTime or datetime object",
    )
