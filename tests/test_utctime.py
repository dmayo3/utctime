from datetime import datetime, timezone, timedelta
import pytest
from utctime import UtcTime, UTC


def test_constructor():
    time = UtcTime(2000, 1, 1, 0, 0, 0)

    assert time == datetime(2000, 1, 1, 0, 0, 0, tzinfo=UTC)
    assert datetime(2000, 1, 1, 0, 0, 0, tzinfo=UTC) == time


def test_timestamp():
    assert UtcTime(1970).timestamp() == 0.0
    assert UtcTime(1971).timestamp() == 365 * 24 * 60 * 60


def test_utc_now():
    current_time = UtcTime.now()

    assert current_time == datetime.fromtimestamp(current_time.timestamp(), tz=UTC)

    assert current_time != datetime.now()
    assert current_time != datetime.utcnow()
    assert current_time != datetime.fromtimestamp(current_time.timestamp())


def test_replace():
    sixoclock = UtcTime(2000, 1, 1).replace(hour=6)
    assert sixoclock == UtcTime(2000, 1, 1, 6)


def test_comparison():
    t1 = UtcTime(2000, 1, 1, 0, 0, 0)
    t2 = UtcTime(2000, 1, 1, 0, 0, 1)
    dt2 = datetime(2000, 1, 1, 0, 0, 1, tzinfo=UTC)
    t3 = UtcTime(2000, 1, 1, 0, 0, 3)

    # No timezone!
    dt4 = datetime(2000, 1, 1, 0, 0, 0)

    assert t1 < t2 < t3
    assert t3 > t2 > t1

    assert t2 == dt2

    assert t1 < dt2 < t3
    assert t3 > dt2 > t1

    assert t1 <= t1 <= t2
    assert t3 >= t3 >= t2

    assert t1 != dt4

    with pytest.raises(TypeError):
        assert t2 < dt4
    with pytest.raises(TypeError):
        assert t2 > dt4


def test_tz_override_prevented():
    with pytest.raises(TypeError):
        UtcTime(2000, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=1)))  # type: ignore

    with pytest.raises(TypeError):
        UtcTime.now(timezone(timedelta(hours=1)))  # type: ignore

    with pytest.raises(TypeError):
        UtcTime.replace(tzinfo=timezone(timedelta(hours=1)))  # type: ignore


def test_utc_type():
    current_time: UtcTime = UtcTime.now()

    assert isinstance(current_time, UtcTime)

    assert not isinstance(current_time, datetime)
    assert not isinstance(datetime.now(), UtcTime)
    assert not issubclass(datetime, UtcTime)


def test_to_datetime():
    current_time: UtcTime = UtcTime.now()
    dt: datetime = current_time.todatetime()

    assert current_time == dt
    assert isinstance(dt, datetime)


def test_format_iso():
    time = UtcTime(2000, 1, 1, 0, 0, 0)

    assert time.iso() == "2000-01-01T00:00:00Z"

    assert str(time) == "UtcTime(2000-01-01T00:00:00Z)"


def test_format_iso_fractional():
    assert UtcTime(2000, 1, 1, 0, 0, 0, 123).iso() == "2000-01-01T00:00:00.000123Z"
    assert UtcTime(2000, 1, 1, 0, 0, 0, 123456).iso() == "2000-01-01T00:00:00.123456Z"


def test_parse_iso():
    expected = UtcTime(2000, 1, 1, 0, 0, 0)

    assert UtcTime.parse_iso("2000-01-01T00:00:00Z") == expected
    assert UtcTime.parse_iso("2000-01-01T00:00:00+00:00") == expected
    assert UtcTime.parse_iso("2000-01-01T05:00:00+05:00") == expected

    with pytest.raises(ValueError):
        UtcTime.parse_iso("2000-01-01T00:00:00")


def test_parse_iso_fractional():
    expected = UtcTime(2000, 1, 1, 0, 0, 0, 123456)

    assert UtcTime.parse_iso("2000-01-01T00:00:00.123456Z") == expected

    with pytest.raises(ValueError):
        UtcTime.parse_iso("2000-01-01T00:00:00.1234567Z")
    with pytest.raises(ValueError):
        UtcTime.parse_iso("2000-01-01T00:00:00.12345678Z")
    with pytest.raises(ValueError):
        UtcTime.parse_iso("2000-01-01T00:00:00.123456789Z")

    expected = UtcTime(2000, 1, 1, 0, 0, 0, 123)

    assert UtcTime.parse_iso("2000-01-01T00:00:00.000123Z") == expected

    assert UtcTime.parse_iso("2000-01-01T00:00:00.123000Z") != expected
    assert UtcTime.parse_iso("2000-01-01T00:00:00.123Z") != expected


def test_add_timedelta():
    hour_later = UtcTime(2000, 1, 1, 6) + timedelta(hours=1)
    assert hour_later == UtcTime(2000, 1, 1, 7)


def test_minus_timedelta():
    hour_before = UtcTime(2000, 1, 1, 6) - timedelta(hours=1)
    assert hour_before == UtcTime(2000, 1, 1, 5)
