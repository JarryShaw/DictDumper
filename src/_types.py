# -*- coding: utf-8 -*-
"""Types compatibility."""

import sys

if sys.version_info.major < 3:
    bytes_type = str
    str_type = unicode
else:
    bytes_type = bytes
    str_type = str
