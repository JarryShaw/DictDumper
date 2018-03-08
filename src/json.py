#!/usr/bin/python3
# -*- coding: utf-8 -*-


import collections
import os
import textwrap


# Writer for JSON files
# Dump a JSON file for PCAP analyser


from jsformat.dumper import Dumper, _type_check


# head
_HEADER_START = '{\n'


# tail
_HEADER_END = '\n}'


# magic types
_MAGIC_TYPES = dict(
    str = lambda self, text, file: self._append_string(text, file),     # string
    bytes = lambda self, text, file: self._append_bytes(text, file),    # string
    datetime = lambda self, text, file: self._append_date(text, file),  # string
    int = lambda self, text, file: self._append_number(text, file),     # number
    float = lambda self, text, file: self._append_number(text, file),   # number
    dict = lambda self, text, file: self._append_object(text, file),    # object
    Info = lambda self, text, file: self._append_object(text, file),    # object
    list = lambda self, text, file: self._append_array(text, file),     # array
    tuple = lambda self, text, file: self._append_array(text, file),    # array
    bool = lambda self, text, file: self._append_bool(text, file),      # true | false
    NoneType = lambda self, text, file: self._append_null(text, file),  # null
)


class JSON(Dumper):
    """Dump JavaScript object notation (JSON) format file.

    Usage:
        >>> dumper = JSON(file_name)
        >>> dumper(content_dict_1, name=content_name_1)
        >>> dumper(content_dict_2, name=content_name_2)
        ............

    Properties:
        * kind - str, return 'json'

    Methods:
        * _dump_header - initially dump file heads and tails
        * _append_value - call this function to write contents

    Attributes:
        * _file - FileIO, output file
        * _sptr - int (file pointer), indicates start of appending point
        * _tctr - int, tab level counter
        * _hrst - str, _HEADER_START
        * _hend - str, _HEADER_END
        * _vctr - dict, value counter dict

    Terminology:
        object    ::=  "{}" | ("{" members "}")
        members   ::=  pair | (pair "," members)
        pair      ::=  string ":" value
        array     ::=  "[]" | ("[" elements "]")
        elements  ::=  value | (value "," elements)
        value     ::=  string | number | object
                         | array | true | false | null

    """
    ##########################################################################
    # Properties.
    ##########################################################################

    @property
    def kind(self):
        """File format of current dumper."""
        return 'json'

    ##########################################################################
    # Attributes.
    ##########################################################################

    _hsrt = _HEADER_START
    _hend = _HEADER_END
    _vctr = collections.defaultdict(int)    # value counter dict

    ##########################################################################
    # Utilities.
    ##########################################################################

    def _append_value(self, value, _file, _name):
        """Call this function to write contents.

        Keyword arguments:
            * value - dict, content to be dunped
            * _file - FileIO, output file
            * _name - str, name of current content dict

        """
        _tabs = '\t' * self._tctr
        _cmma = ',\n' if self._vctr[self._tctr] else ''
        _keys = '{cmma}{tabs}"{name}" :'.format(cmma=_cmma, tabs=_tabs, name=_name)

        _file.seek(self._sptr, os.SEEK_SET)
        _file.write(_keys)

        self._vctr[self._tctr] += 1
        self._append_object(value, _file)

    ##########################################################################
    # Functions.
    ##########################################################################

    def _append_array(self, value, _file):
        """Call this function to write array contents.

        Keyword arguments:
            * value - dict, content to be dunped
            * _file - FileIO, output file

        """
        _labs = ' ['
        _file.write(_labs)

        self._tctr += 1

        for _item in value:
            _cmma = ',' if self._vctr[self._tctr] else ''
            _file.write(_cmma)

            self._vctr[self._tctr] += 1

            _type = type(_item).__name__
            _MAGIC_TYPES[_type](self, _item, _file)

        self._vctr[self._tctr] = 0
        self._tctr -= 1

        _labs = ' ]'
        _file.write(_labs)

    def _append_object(self, value, _file):
        """Call this function to write object contents.

        Keyword arguments:
            * value - dict, content to be dunped
            * _file - FileIO, output file

        """
        _labs = ' {'
        _file.write(_labs)
        self._tctr += 1

        for (_item, _text) in value.items():
            _tabs = '\t' * self._tctr
            _cmma = ',' if self._vctr[self._tctr] else ''
            _keys = '{cmma}\n{tabs}"{item}" :'.format(cmma=_cmma, tabs=_tabs, item=_item)
            _file.write(_keys)

            self._vctr[self._tctr] += 1

            _type = _type_check(_text)
            _MAGIC_TYPES[_type](self, _text, _file)

        self._vctr[self._tctr] = 0
        self._tctr -= 1
        _tabs = '\t' * self._tctr
        _labs = '\n{tabs}{}'.format('}', tabs=_tabs)
        _file.write(_labs)

    def _append_string(self, value, _file):
        """Call this function to write string contents.

        Keyword arguments:
            * value - dict, content to be dunped
            * _file - FileIO, output file

        """
        _text = value
        _labs = ' "{text}"'.format(text=_text)
        _file.write(_labs)

    def _append_bytes(self, value, _file):
        """Call this function to write bytes contents.

        Keyword arguments:
            * value - dict, content to be dunped
            * _file - FileIO, output file

        """
        # binascii.b2a_base64(value) -> plistlib.Data
        # binascii.a2b_base64(Data) -> value(bytes)

        _text = ' '.join(textwrap.wrap(value.hex(), 2))
        # _data = [H for H in iter(
        #         functools.partial(io.StringIO(value.hex()).read, 2), '')
        #         ]  # to split bytes string into length-2 hex string list
        _labs = ' "{text}"'.format(text=_text)
        _file.write(_labs)

    def _append_date(self, value, _file):
        """Call this function to write date contents.

        Keyword arguments:
            * value - dict, content to be dunped
            * _file - FileIO, output file

        """
        _text = value.strftime('%Y-%m-%dT%H:%M:%SZ')
        _labs = ' "{text}"'.format(text=_text)
        _file.write(_labs)

    def _append_number(self, value, _file):
        """Call this function to write number contents.

        Keyword arguments:
            * value - dict, content to be dunped
            * _file - FileIO, output file

        """
        _text = value
        _labs = ' {text}'.format(text=_text)
        _file.write(_labs)

    def _append_bool(self, value, _file):
        """Call this function to write bool contents.

        Keyword arguments:
            * value - dict, content to be dunped
            * _file - FileIO, output file

        """
        _text = 'true' if value else 'false'
        _labs = ' {text}'.format(text=_text)
        _file.write(_labs)

    def _append_null(self, value, _file):
        """Call this function to write null contents.

        Keyword arguments:
            * value - dict, content to be dunped
            * _file - FileIO, output file

        """
        _text = 'null'
        _labs = ' {text}'.format(text=_text)
        _file.write(_labs)
