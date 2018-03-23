# -*- coding: utf-8 -*-
"""dumper a PLIST file

``jsformat.plist`` contains ``PLIST`` only, which dumpers an
Apple property list (PLIST) file. Usage sample is described
as below.

    >>> dumper = PLIST(file_name)
    >>> dumper(content_dict_1, name=content_name_1)
    >>> dumper(content_dict_2, name=content_name_2)
    ............

"""
import os
import textwrap


# Dumper for PLIST files
# Write a macOS Property List file


from jsformat.dumper import _type_check
from jsformat.xml import XML


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


# magic types
_MAGIC_TYPES = dict(
    list = lambda self, text, file: self._append_array(text, file),         # array
    tuple = lambda self, text, file: self._append_array(text, file),        # array
    dict = lambda self, text, file: self._append_dict(text, file),          # dict
    Info = lambda self, text, file: self._append_dict(text, file),          # dict
    str = lambda self, text, file: self._append_string(text, file),         # string
    bytes = lambda self, text, file: self._append_data(text, file),         # data
    datetime = lambda self, text, file: self._append_date(text, file),      # date
    int = lambda self, text, file: self._append_integer(text, file),        # integer
    float = lambda self, text, file: self._append_real(text, file),         # real
    bool = lambda self, text, file: self._append_bool(text, file),          # true | false
    NoneType = lambda self, text, file: self._append_string(text, file),    # string
)


class PLIST(XML):
    """Dump Apple property list (PLIST) format file.

    Usage:
        >>> dumper = PLIST(file_name)
        >>> dumper(content_dict_1, name=content_name_1)
        >>> dumper(content_dict_2, name=content_name_2)
        ............

    Properties:
        * kind - str, return 'plist'

    Methods:
        * _dump_header - initially dump file heads and tails
        * _append_value - call this function to write contents

    Attributes:
        * _file - FileIO, output file
        * _sptr - int (file pointer), indicates start of appending point
        * _tctr - int, tab level counter
        * _hrst - str, _HEADER_START
        * _hend - str, _HEADER_END

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
    # Attributes.
    ##########################################################################

    _hsrt = _HEADER_START
    _hend = _HEADER_END

    ##########################################################################
    # Utilities.
    ##########################################################################

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

    def _append_array(self, value, _file):
        """Call this function to write array contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _tabs = '\t' * self._tctr
        _labs = '{tabs}<array>\n'.format(tabs=_tabs)
        _file.write(_labs)
        self._tctr += 1

        for _item in value:
            if _item is None:   continue
            _type = type(_item).__name__
            _MAGIC_TYPES[_type](self, _item, _file)

        self._tctr -= 1
        _tabs = '\t' * self._tctr
        _labs = '{tabs}</array>\n'.format(tabs=_tabs)
        _file.write(_labs)

    def _append_dict(self, value, _file):
        """Call this function to write dict contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _tabs = '\t' * self._tctr
        _labs = '{tabs}<dict>\n'.format(tabs=_tabs)
        _file.write(_labs)
        self._tctr += 1

        for (_item, _text) in value.items():
            if _text is None:   continue

            _tabs = '\t' * self._tctr
            _keys = '{tabs}<key>{item}</key>\n'.format(tabs=_tabs, item=_item)
            _file.write(_keys)

            _type = _type_check(_text)
            _MAGIC_TYPES[_type](self, _text, _file)

        self._tctr -= 1
        _tabs = '\t' * self._tctr
        _labs = '{tabs}</dict>\n'.format(tabs=_tabs)
        _file.write(_labs)

    def _append_string(self, value, _file):
        """Call this function to write string contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _tabs = '\t' * self._tctr
        _text = value or 'N/A'
        _labs = '{tabs}<string>{text}</string>\n'.format(tabs=_tabs, text=_text)
        _file.write(_labs)

    def _append_data(self, value, _file):
        """Call this function to write data contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        # binascii.b2a_base64(value) -> plistlib.Data
        # binascii.a2b_base64(Data) -> value(bytes)

        _tabs = '\t' * self._tctr
        _labs = '{tabs}<data>\n'.format(tabs=_tabs)

        _list = []
        for _item in textwrap.wrap(value.hex(), 32):
            _text = ' '.join(textwrap.wrap(_item, 2))
            _item = '{tabs}\t{text}'.format(tabs=_tabs, text=_text)
            _list.append(_item)
        _labs += '\n'.join(_list)
        # _data = [H for H in iter(
        #         functools.partial(io.StringIO(value.hex()).read, 2), '')
        #         ]  # to split bytes string into length-2 hex string list
        _labs += '\n{tabs}</data>\n'.format(tabs=_tabs)
        _file.write(_labs)

    def _append_date(self, value, _file):
        """Call this function to write date contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _tabs = '\t' * self._tctr
        _text = value.strftime('%Y-%m-%dT%H:%M:%SZ')
        _labs = '{tabs}<date>{text}</date>\n'.format(tabs=_tabs, text=_text)
        _file.write(_labs)

    def _append_integer(self, value, _file):
        """Call this function to write integer contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _tabs = '\t' * self._tctr
        _text = value
        _labs = '{tabs}<integer>{text}</integer>\n'.format(tabs=_tabs, text=_text)
        _file.write(_labs)

    def _append_real(self, value, _file):
        """Call this function to write real contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _tabs = '\t' * self._tctr
        _text = value
        _labs = '{tabs}<real>{text}</real>\n'.format(tabs=_tabs, text=_text)
        _file.write(_labs)

    def _append_bool(self, value, _file):
        """Call this function to write bool contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _tabs = '\t' * self._tctr
        _text = '<true/>' if value else '<false/>'
        _labs = '{tabs}{text}\n'.format(tabs=_tabs, text=_text)
        _file.write(_labs)
