# -*- coding: utf-8 -*-
"""Binary data processing utilities."""

import binascii


def hexlify(s):
    """Hexadecimal representation of binary data."""
    if hasattr(s, 'hex'):
        return s.hex()
    return binascii.hexlify(s).decode()
