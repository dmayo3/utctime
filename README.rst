UTC Time v0.1.1-alpha
-------------------

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


Checkout the docs link below for more information.

:Install: `PyPi <https://pypi.org/project/utctime>`_
:Docs:    `Read The Docs <https://utctime.readthedocs.io>`_
:License: `MIT <https://github.com/dmayo3/utctime/blob/main/LICENSE>`_
:Source:  `GitHub <https://github.com/dmayo3/utctime>`_
:Issues:  `GitHub Issues <https://github.com/dmayo3/utctime/issues>`_
