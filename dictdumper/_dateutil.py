# -*- coding: utf-8 -*-
"""Date & time processing utilities."""

import datetime

__all__ = ['isoformat']

try:
    from datetime import _format_time
except ImportError:
    def _format_time(hh, mm, ss, us, timespec='auto'):
        specs = {
            'hours': '{:02d}',
            'minutes': '{:02d}:{:02d}',
            'seconds': '{:02d}:{:02d}:{:02d}',
            'milliseconds': '{:02d}:{:02d}:{:02d}.{:03d}',
            'microseconds': '{:02d}:{:02d}:{:02d}.{:06d}'
        }

        if timespec == 'auto':
            # Skip trailing microseconds when us==0.
            timespec = 'microseconds' if us else 'seconds'
        elif timespec == 'milliseconds':
            us //= 1000
        try:
            fmt = specs[timespec]
        except KeyError:
            raise ValueError('Unknown timespec value')
        else:
            return fmt.format(hh, mm, ss, us)

try:
    from datetime import _format_offset
except ImportError:
    def _format_offset(off):
        s = ''
        if off is not None:
            if off.days < 0:
                sign = "-"
                off = -off
            else:
                sign = "+"
            hh, mm = divmod(off, datetime.timedelta(hours=1))
            mm, ss = divmod(mm, datetime.timedelta(minutes=1))
            s += "%s%02d:%02d" % (sign, hh, mm)
            if ss or ss.microseconds:
                s += ":%02d" % ss.seconds

                if ss.microseconds:
                    s += '.%06d' % ss.microseconds
        return s


def isoformat(date):
    """Generate ISO format date string."""
    if hasattr(date, 'isoformat'):
        return date.isoformat()
    if isinstance(date, datetime.date):
        return "%04d-%02d-%02d" % (date.year, date.month, date.day)
    if isinstance(date, datetime.time):
        s = _format_time(date.hour, date.minute, date.second,
                         date.microsecond, 'auto')
        off = date.utcoffset()
        tz = _format_offset(off)
        if tz:
            s += tz
        return s
    if isinstance(date, datetime.datetime):
        s = ("%04d-%02d-%02d%c" % (date.year, date.month, date.day, 'T') +
             _format_time(date.hour, date.minute, date.second,
                          date.microsecond, 'auto'))

        off = date.utcoffset()
        tz = _format_offset(off)
        if tz:
            s += tz

        return s
    raise NotImplementedError('unknown date object: %s' % date)
