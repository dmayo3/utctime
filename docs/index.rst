UTC Time
========

This is a tiny utility to simplify the everyday pain of working with UTC datetimes
and ISO 8601 strings in Python.


Motivation
----------

1. **Easy**: create UTC datetimes without thinking about it.

2. **Type-safe**: don't accidentally mix and match UTC with non-UTC or naive datetimes.

3. **ISO 8601**: convert to and from ISO 8601 datetimes with ease (and use `Z` as the timezone instead of `+00:00`).

4. **Safe Format**: don't accidentally convert to anything else.

5. **Flexible Parsing**: parses various ISO 8601 formats - with/without microseconds and/or with `Z` or `+HH:MM` timezones.

6. **No Dependencies**. we don't need to pull in `pytz` just for UTC.

7. **Interoperate**: with regular `datetime` objects where necessary.

8. **Familiar**: similar names and conventions to working with `datetime`.


Usage
-----

.. doctest::

   >>> from utctime import UtcTime

   >>> UtcTime.now()
   UtcTime(...)

   >>> UtcTime(2030).todatetime()
   datetime.datetime(2030, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

   >>> UtcTime(2030)
   UtcTime(2030-01-01T00:00:00Z)

   >>> UtcTime(2030).iso()
   '2030-01-01T00:00:00Z'

   >>> UtcTime.parse_iso("2030-01-01T00:00:00Z")
   UtcTime(2030-01-01T00:00:00Z)

   >>> UtcTime.parse_iso("2030-01-01T06:0:00.000+02:00")
   UtcTime(2030-01-01T04:00:00Z)

   >>> UtcTime(1999).year
   1999
   >>> UtcTime(1970, 5).month
   5
   >>> UtcTime(1980, 3, 13).day
   13

   >>> UtcTime(1970, 1, 1).timestamp()
   0.0

   >>> UtcTime(1970) < UtcTime(1980)
   True
   >>> UtcTime(1980) == UtcTime(1981)
   False
   >>> UtcTime(1981) > UtcTime(1980)
   True


You can also compare with datetimes, add/subtract timedeltas, replace fields, and convert from datetimes.

See the API reference for full details.


Contents
--------

.. toctree::

   api
