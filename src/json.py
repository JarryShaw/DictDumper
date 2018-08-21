# -*- coding: utf-8 -*-
"""dumper a JSON file

``dictdumper.json`` contains ``JSON`` only, which dumpers a
JavaScript object notation (JSON) file. Usage sample is
described as below.

    >>> dumper = JSON(file_name)
    >>> dumper(content_dict_1, name=content_name_1)
    >>> dumper(content_dict_2, name=content_name_2)
    ............

"""
import collections
import datetime
import os
import textwrap


# Writer for JSON files
# Dump a JSON file for PCAP analyser


from dictdumper.dumper import Dumper


# head
_HEADER_START = '{\n'


# tail
_HEADER_END = '\n}'


# magic types
_MAGIC_TYPES = collections.defaultdict(
    lambda : (lambda self, text, file: self._append_string(text, file)), dict(
    # string
    str = lambda self, text, file: self._append_string(text, file),

    # bytes
    bytes = lambda self, text, file: self._append_bytes(text, file),
    bytearray = lambda self, text, file: self._append_bytes(text, file),
    memoryview = lambda self, text, file: self._append_bytes(text, file),

    # date
    datetime = lambda self, text, file: self._append_date(text, file),

    # number
    int = lambda self, text, file: self._append_number(text, file),
    float = lambda self, text, file: self._append_number(text, file),

    # object
    dict = lambda self, text, file: self._append_object(text, file),

    # array
    list = lambda self, text, file: self._append_array(text, file),
    tuple = lambda self, text, file: self._append_array(text, file),
    range = lambda self, text, file: self._append_array(text, file),
    set = lambda self, text, file: self._append_array(text, file),
    frozenset = lambda self, text, file: self._append_array(text, file),

    # bool
    bool = lambda self, text, file: self._append_bool(text, file),

    # null
    NoneType = lambda self, text, file: self._append_null(text, file),
))


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
        * object_hook - default/customised object hooks

    Attributes:
        * _file - FileIO, output file
        * _sptr - int (file pointer), indicates start of appending point
        * _tctr - int, tab level counter
        * _hrst - str, _HEADER_START
        * _hend - str, _HEADER_END
        * _vctr - dict, value counter dict

    Utilities:
        * _dump_header - initially dump file heads and tails
        * _append_value - call this function to write contents

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
    # Type codes.
    ##########################################################################

    __type__ = (
        str,                                    # stinrg
        bool,                                   # bool
        dict,                                   # object
        datetime.date,                          # date
        int, float, complex,                    # number
        type(None),                             # null
        bytes, bytearray, memoryview,           # bytes
        list, tuple, range, set, frozenset,     # array
    )

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
            * value - dict, content to be dumped
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
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _labs = ' ['
        _file.write(_labs)

        self._tctr += 1

        for _item in value:
            _cmma = ',' if self._vctr[self._tctr] else ''
            _file.write(_cmma)

            self._vctr[self._tctr] += 1

            _item = self.object_hook(_item)
            _type = type(_item).__name__
            _MAGIC_TYPES[_type](self, _item, _file)

        self._vctr[self._tctr] = 0
        self._tctr -= 1

        _labs = ' ]'
        _file.write(_labs)

    def _append_object(self, value, _file):
        """Call this function to write object contents.

        Keyword arguments:
            * value - dict, content to be dumped
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

            _text = self.object_hook(_text)
            _type = type(_text).__name__
            _MAGIC_TYPES[_type](self, _text, _file)

        self._vctr[self._tctr] = 0
        self._tctr -= 1
        _tabs = '\t' * self._tctr
        _labs = '\n{tabs}{}'.format('}', tabs=_tabs)
        _file.write(_labs)

    def _append_string(self, value, _file):
        """Call this function to write string contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _text = str(value).replace('"', '\\"')
        _labs = ' "{text}"'.format(text=_text)
        _file.write(_labs)

    def _append_bytes(self, value, _file):
        """Call this function to write bytes contents.

        Keyword arguments:
            * value - dict, content to be dumped
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
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _text = value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        _labs = ' "{text}"'.format(text=_text)
        _file.write(_labs)

    def _append_number(self, value, _file):
        """Call this function to write number contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _text = value
        _labs = ' {text}'.format(text=_text)
        _file.write(_labs)

    def _append_bool(self, value, _file):
        """Call this function to write bool contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _text = 'true' if value else 'false'
        _labs = ' {text}'.format(text=_text)
        _file.write(_labs)

    def _append_null(self, value, _file):
        """Call this function to write null contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _text = 'null'
        _labs = ' {text}'.format(text=_text)
        _file.write(_labs)
