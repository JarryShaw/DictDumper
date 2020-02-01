# -*- coding: utf-8 -*-
"""dumper a PLIST file

``dictdumper.plist`` contains ``PLIST`` only, which dumpers an
Apple property list (PLIST) file. Usage sample is described
as below.

    >>> dumper = PLIST(file_name)
    >>> dumper(content_dict_1, name=content_name_1)
    >>> dumper(content_dict_2, name=content_name_2)
    ............

"""
# Dumper for PLIST files
# Write a macOS Property List file

import base64
import datetime
import os

from dictdumper._types import bytes_type, str_type
from dictdumper.xml import XML

__all__ = ['PLIST']

# head
_HEADER_START = '''\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
'''

# tail
_HEADER_END = '''\
</dict>
</plist>
'''


class PLIST(XML):
    """Dump Apple property list (PLIST) format file.

    Usage:
        >>> dumper = PLIST(file_name)
        >>> dumper(content_dict_1, name=content_name_1)
        >>> dumper(content_dict_2, name=content_name_2)
        ............

    Properties:
        * kind - str, return 'plist'
        * filename - str, output file name

    Methods:
        * make_object - create an object with convertion information
        * object_hook - convert content for function call
        * default - check content type for function call

    Attributes:
        * _file - str, output file name
        * _sptr - int (file pointer), indicates start of appending point
        * _tctr - int, tab level counter
        * _hrst - str, _HEADER_START
        * _hend - str, _HEADER_END

    Utilities:
        * _dump_header - initially dump file heads and tails
        * _encode_func - check content type for function call
        * _encode_value - convert content for function call
        * _append_value - call this function to write contents

    Terminology:
        value    ::=  array | dict | string | data
                        | date | integer | real | bool
        array    ::=  "<array>" value* "</array>"
        dict     ::=  "<dict>" ("<key>" str "</key>" value)* "</dict>"
        string   ::=  "<string>" str "</string>"
        data     ::=  "<data>" bytes "</data>"
        date     ::=  "<date>" datetime "</date>"
        integer  ::=  "<integer>" int "</integer>"
        real     ::=  "<real>" float "</real>"
        bool     ::=  "<true/>" | "<false/>"

    """
    ##########################################################################
    # Properties.
    ##########################################################################

    @property
    def kind(self):
        """File format of current dumper."""
        return 'plist'

    ##########################################################################
    # Type codes.
    ##########################################################################

    __type__ = (
        # string
        (str_type, 'string'),

        # bool
        (bool, 'bool'),

        # dict
        (dict, 'dict'),

        # date
        (datetime.date, 'date'),
        (datetime.datetime, 'date'),

        # integer
        (int, 'integer'),

        # real
        (float, 'real'),

        # data
        (bytes_type, 'data'),

        # array
        (list, 'array'),
    )

    ##########################################################################
    # Attributes.
    ##########################################################################

    _hsrt = _HEADER_START
    _hend = _HEADER_END

    ##########################################################################
    # Utilities.
    ##########################################################################

    def _encode_value(self, o):  # pylint: disable=unused-argument
        """Convert content for function call."""
        if o is None:
            return self.make_object(o, 'None')
        if isinstance(o, bytearray):
            return self.make_object(o, bytes_type(o))
        if isinstance(o, memoryview):
            return self.make_object(o, o.tobytes())
        if isinstance(o, (tuple, set, frozenset)):
            return self.make_object(o, list(o))
        return o

    def _append_value(self, value, _file, _name):
        """Call this function to write contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file
            * _name - str, name of current content dict

        """
        _tabs = '\t' * self._tctr
        _keys = '{tabs}<key>{name}</key>\n'.format(tabs=_tabs, name=_name)
        _file.seek(self._sptr, os.SEEK_SET)
        _file.write(_keys)

        self._append_dict(value, _file)

    ##########################################################################
    # Functions.
    ##########################################################################

    def _append_dict(self, value, file):
        """Call this function to write dict contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * file - FileIO, output file

        """
        tabs = '\t' * self._tctr
        labs = '{tabs}<dict>\n'.format(tabs=tabs)
        file.write(labs)
        self._tctr += 1

        for (item, text) in value.items():
            if text is None:
                continue

            tabs = '\t' * self._tctr
            keys = '{tabs}<key>{item}</key>\n'.format(tabs=tabs, item=item)
            file.write(keys)

            enc_text = self._encode_value(text)
            func = self._encode_func(enc_text)
            func(enc_text, file)

        self._tctr -= 1
        tabs = '\t' * self._tctr
        labs = '{tabs}</dict>\n'.format(tabs=tabs)
        file.write(labs)

    def _append_array(self, value, file):
        """Call this function to write array contents.

        Keyword arguments:
            * value - list, content to be dumped
            * file - FileIO, output file

        """
        tabs = '\t' * self._tctr
        labs = '{tabs}<array>\n'.format(tabs=tabs)
        file.write(labs)
        self._tctr += 1

        for item in value:
            if item is None:
                continue

            enc_text = self._encode_value(item)
            func = self._encode_func(enc_text)
            func(enc_text, file)

        self._tctr -= 1
        tabs = '\t' * self._tctr
        labs = '{tabs}</array>\n'.format(tabs=tabs)
        file.write(labs)

    def _append_string(self, value, file):
        """Call this function to write string contents.

        Keyword arguments:
            * value - str, content to be dumped
            * file - FileIO, output file

        """
        tabs = '\t' * self._tctr
        text = value
        labs = '{tabs}<string>{text}</string>\n'.format(tabs=tabs, text=text)
        file.write(labs)

    def _append_data(self, value, file):
        """Call this function to write data contents.

        Keyword arguments:
            * value - bytes, content to be dumped
            * file - FileIO, output file

        """
        # binascii.b2a_base64(value) -> plistlib.Data
        # binascii.a2b_base64(Data) -> value(bytes)

        tabs = '\t' * self._tctr
        text = base64.b64encode(value).decode()
        labs = '{tabs}<data>{text}</data>\n'.format(tabs=tabs, text=text)
        file.write(labs)

    def _append_date(self, value, file):
        """Call this function to write date contents.

        Keyword arguments:
            * value - Union[date, datetime], content to be dumped
            * file - FileIO, output file

        """
        tabs = '\t' * self._tctr
        text = value.strftime(r'%Y-%m-%dT%H:%M:%S.%fZ')
        labs = '{tabs}<date>{text}</date>\n'.format(tabs=tabs, text=text)
        file.write(labs)

    def _append_integer(self, value, file):
        """Call this function to write integer contents.

        Keyword arguments:
            * value - int, content to be dumped
            * file - FileIO, output file

        """
        tabs = '\t' * self._tctr
        text = value
        labs = '{tabs}<integer>{text}</integer>\n'.format(tabs=tabs, text=text)
        file.write(labs)

    def _append_real(self, value, file):
        """Call this function to write real contents.

        Keyword arguments:
            * value - float, content to be dumped
            * file - FileIO, output file

        """
        tabs = '\t' * self._tctr
        text = value
        labs = '{tabs}<real>{text}</real>\n'.format(tabs=tabs, text=text)
        file.write(labs)

    def _append_bool(self, value, file):
        """Call this function to write bool contents.

        Keyword arguments:
            * value - bool, content to be dumped
            * file - FileIO, output file

        """
        tabs = '\t' * self._tctr
        text = '<true/>' if value else '<false/>'
        labs = '{tabs}{text}\n'.format(tabs=tabs, text=text)
        file.write(labs)
