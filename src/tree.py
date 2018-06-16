# -*- coding: utf-8 -*-
"""dumper a tree-view file

``jsformat.tree`` contains ``Tree`` only, which dumpers a
tree-view text (TXT) format file. Usage sample is described
as below.

    >>> dumper = Tree(file_name)
    >>> dumper(content_dict_1, name=content_name_1)
    >>> dumper(content_dict_2, name=content_name_2)
    ............

"""
import collections
import os
import textwrap


# Writer for treeview text files
# Dump a TEXT file for PCAP analyser


from jsformat.dumper import Dumper, _type_check


# headers
_HEADER_START = 'PCAP File Tree-View Format\n'   # head
_HEADER_END = ''                               # tail


# templates
_TEMP_BRANCH = '  |   '  # branch
_TEMP_SPACES = '      '  # space


# magic types
_MAGIC_TYPES = dict(
    dict = lambda self, text, file: self._append_branch(text, file),    # branch
    list = lambda self, text, file: self._append_array(text, file),     # array
    tuple = lambda self, text, file: self._append_array(text, file),    # array
    str = lambda self, text, file: self._append_string(text, file),     # string
    bytes = lambda self, text, file: self._append_bytes(text, file),    # string
    datetime = lambda self, text, file: self._append_date(text, file),  # string
    int = lambda self, text, file: self._append_number(text, file),     # number
    float = lambda self, text, file: self._append_number(text, file),   # number
    bool = lambda self, text, file: self._append_bool(text, file),      # True | False
    NoneType = lambda self, text, file: self._append_none(text, file),  # N/A
)


class Tree(Dumper):
    """Dump a tree-view text (TXT) format file.

    Usage:
        >>> dumper = Tree(file_name)
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
        * _bctr - dict, blank branch counter dict

    Terminology:
        value   ::=  branch | array | string | number | bool | N/A
        string
          |-- string
          |     |-- string -> value
          |     |-- string
          |     |     |-- string -> value
          |     |     |-- string -> value
          |     |-- string -> value
          |     |-- string -> value
          |           |-- string -> value
          |           |-- string -> value
          |-- string -> value, value, value
          |-- string -> True
          |-- string -> False
          |-- string -> N/A
          |-- string -> value
          |-- string -> value

    """
    ##########################################################################
    # Attributes.
    ##########################################################################

    _tctr = -1
    _hsrt = _HEADER_START
    _hend = _HEADER_END

    ##########################################################################
    # Properties.
    ##########################################################################

    @property
    def kind(self):
        """File format of current dumper."""
        return 'txt'

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
        _keys = '\n' + _name + '\n'
        _file.seek(self._sptr, os.SEEK_SET)
        _file.write(_keys)

        self._bctr = collections.defaultdict(int)    # blank branch counter dict
        self._append_branch(value, _file)

    def _append_array(self, value, _file):
        """Call this function to write array contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        if not value:
            self._append_none(None, _file)

        _bptr = ''
        _tabs = ''
        _tlen = len(value) - 1
        if _tlen:
            _bptr = '  |-->'
            for _ in range(self._tctr + 1):
                _tabs += _TEMP_SPACES if self._bctr[_] else _TEMP_BRANCH

        for (_nctr, _item) in enumerate(value):
            _text = '{tabs}{bptr}'.format(tabs=_tabs, bptr=_bptr)
            _file.write(_text)

            _type = _type_check(_text)
            _MAGIC_TYPES[_type](self, _item, _file)

            _suff = '\n' if _nctr < _tlen else ''
            _file.write(_suff)

    def _append_branch(self, value, _file):
        """Call this function to write branch contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        if not value:
            self._append_none(None, _file)

        self._tctr += 1
        _vlen = len(value)
        for (_vctr, (_item, _text)) in enumerate(value.items()):
            _type = _type_check(_text)

            flag_dict = (_type == 'dict')
            flag_tuple = (_type == 'tuple' and len(_text) > 1)
            flag_bytes = (_type == 'bytes' and len(_text) > 16)
            if any((flag_dict, flag_tuple, flag_bytes)):
                _pref = '\n'
            else:
                _pref = ' ->'

            _labs = ''
            for _ in range(self._tctr):
                _labs += _TEMP_SPACES if self._bctr[_] else _TEMP_BRANCH

            _keys = '{labs}  |-- {item}{pref}'.format(labs=_labs, item=_item, pref=_pref)
            _file.write(_keys)

            if _vctr == _vlen - 1:
                self._bctr[self._tctr] = 1

            _MAGIC_TYPES[_type](self, _text, _file)

            _suff = '' if _type == 'dict' else '\n'
            _file.write(_suff)

        self._bctr[self._tctr] = 0
        self._tctr -= 1

    def _append_string(self, value, _file):
        """Call this function to write string contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        if not value:
            self._append_none(None, _file)

        _text = value or 'NULL'
        _labs = ' {text}'.format(text=_text)
        _file.write(_labs)

    def _append_bytes(self, value, _file):
        """Call this function to write bytes contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        # binascii.b2a_base64(value) -> plistlib.Data
        # binascii.a2b_base64(Data) -> value(bytes)
        if not value:
            self._append_none(None, _file)

        if len(value) > 16:
            _tabs = ''
            for _ in range(self._tctr + 1):
                _tabs += _TEMP_SPACES if self._bctr[_] else _TEMP_BRANCH

            _list = []
            for (_ictr, _item) in enumerate(textwrap.wrap(value.hex(), 32)):
                _bptr = '       ' if _ictr else '  |--> '
                _text = ' '.join(textwrap.wrap(_item, 2))
                _item = '{tabs}{bptr}{text}'.format(tabs=_tabs, bptr=_bptr, text=_text)
                _list.append(_item)
            _labs = '\n'.join(_list)
        else:
            _text = ' '.join(textwrap.wrap(value.hex(), 2))
            _labs = ' {text}'.format(text=_text)
        _file.write(_labs)

    def _append_date(self, value, _file):
        """Call this function to write date contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _text = value.strftime('%Y-%m-%d %H:%M:%S.%f')
        _labs = ' {text}'.format(text=_text)
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
        _text = 'True' if value else 'False'
        _labs = ' {text}'.format(text=_text)
        _file.write(_labs)

    def _append_none(self, value, _file):
        """Call this function to write none contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * _file - FileIO, output file

        """
        _text = 'NIL'
        _labs = ' {text}'.format(text=_text)
        _file.write(_labs)
