# -*- coding: utf-8 -*-
"""dumper a tree-view file

``dictdumper.tree`` contains ``Tree`` only, which dumpers a
tree-view text (TXT) format file. Usage sample is described
as below.

    >>> dumper = Tree(filename)
    >>> dumper(content_dict_1, name=contentname_1)
    >>> dumper(content_dict_2, name=contentname_2)
    ............

"""
# Writer for treeview text files
# Dump a TEXT file for PCAP analyser

from __future__ import unicode_literals

import contextlib
import datetime
import math
import os
import textwrap

from dictdumper._dateutil import isoformat
from dictdumper._hexlify import hexlify
from dictdumper._types import bytes_type, str_type
from dictdumper.dumper import Dumper

__all__ = ['Tree']

# headers
_HEADER_START = ''  # head
_HEADER_END = ''    # tail

# templates
_TEMP_BRANCH = '  |   '  # branch
_TEMP_SPACES = '      '  # space


@contextlib.contextmanager
def indent(ctx, branch=True):
    """Indentation context."""
    if branch:
        ctx.append(_TEMP_BRANCH)
    else:
        ctx.append(_TEMP_SPACES)
    yield
    ctx.pop()


try:
    from contextlib import nullcontext
except ImportError:
    class nullcontext:
        """Context manager that does no additional processing."""
        def __enter__(self):
            return self
        def __exit__(self, *excinfo):
            pass


class Tree(Dumper):
    """Dump a tree-view text (TXT) format file.

    Usage:
        >>> dumper = Tree(filename)
        >>> dumper(content_dict_1, name=contentname_1)
        >>> dumper(content_dict_2, name=contentname_2)
        ............

    Properties:
        * kind - str, file format of current dumper
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
        * _bctx - list, blank branch context record
        * _nctr - int, branch number counter

    Utilities:
        * _dump_header - initially dump file heads and tails
        * _encode_func - check content type for function call
        * _encode_value - convert content for function call
        * _append_value - call this function to write contents

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
    # Properties.
    ##########################################################################

    @property
    def kind(self):
        """File format of current dumper."""
        return 'txt'

    ##########################################################################
    # Type codes.
    ##########################################################################

    __type__ = (
        # string
        (str_type, 'string'),

        # bool
        (bool, 'bool'),

        # branch
        (dict, 'branch'),

        # none
        (type(None), 'none'),

        # date
        (datetime.date, 'date'),
        (datetime.datetime, 'date'),
        (datetime.time, 'date'),

        # number
        (int, 'number'),
        (float, 'number'),
        (complex, 'number'),

        # bytes
        (bytes_type, 'bytes'),

        # array
        (list, 'array'),
    )

    ##########################################################################
    # Methods.
    ##########################################################################

    @staticmethod
    def check_newline(value):
        """Check if newline is needed."""
        if isinstance(value, dict):
            return True
        if isinstance(value, str_type):
            return len(value) > 2
        if isinstance(value, bytes_type):
            return len(hexlify(value)) > 32
        return False

    ##########################################################################
    # Attributes.
    ##########################################################################

    _nctr = 0
    _bctx = ''

    _hsrt = _HEADER_START
    _hend = _HEADER_END

    ##########################################################################
    # Utilities.
    ##########################################################################

    def _encode_value(self, o):  # pylint: disable=unused-argument
        """Convert content for function call."""
        if isinstance(o, bytearray):
            return self.make_object(o, bytes_type(o), text=o.decode(errors='replace'))
        if isinstance(o, memoryview):
            tobytes = o.tobytes()
            return self.make_object(o, tobytes, text=tobytes.decode(errors='replace'))
        if isinstance(o, (tuple, set, frozenset)):
            return self.make_object(o, list(o))
        return o

    def _append_value(self, value, file, name):
        """Call this function to write contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * file - FileIO, output file
            * name - str, name of current content dict

        """
        file.seek(self._sptr, os.SEEK_SET)
        if self._nctr > 0:
            file.write('\n')
        file.write(name)

        self._bctx = list()  # blank branch indent context
        self._append_branch(value, file)

        self._nctr += 1
        file.write('\n')

    ##########################################################################
    # Functions.
    ##########################################################################

    def _append_branch(self, value, file):  # pylint: disable=inconsistent-return-statements
        """Call this function to write branch contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * file - FileIO, output file

        """
        if not value:
            file.write(' ')
            return self._append_none(None, file)

        vlen = len(value)
        for (vctr, (item, text)) in enumerate(value.items(), start=1):
            file.write('\n' + ''.join(self._bctx))
            file.write('  |-- {item} '.format(item=item))

            with indent(self._bctx, branch=vctr != vlen):
                enc_text = self._encode_value(text)
                func = self._encode_func(enc_text)
                func(enc_text, file)

    def _append_array(self, value, file):  # pylint: disable=inconsistent-return-statements
        """Call this function to write array contents.

        Keyword arguments:
            * value - list, content to be dumped
            * file - FileIO, output file

        """
        if not value:
            file.write(' ')
            return self._append_none(None, file)

        vlen = len(value)
        for (vctr, item) in enumerate(value, start=1):
            file.write('\n' + ''.join(self._bctx) + '  |-')

            if vctr != vlen:
                ctx = indent(self._bctx)
            else:
                ctx = nullcontext()

            with ctx:
                enc_text = self._encode_value(item)

                if self.check_newline(enc_text):
                    file.write('-> --')

                func = self._encode_func(enc_text)
                func(enc_text, file)

    def _append_string(self, value, file):  # pylint: disable=inconsistent-return-statements
        """Call this function to write string contents.

        Keyword arguments:
            * value - str, content to be dumped
            * file - FileIO, output file

        """
        if not value:
            file.write(' ')
            return self._append_none(None, file)

        if len(value) <= 40:
            labs = '-> {text}'.format(text=value)
        else:
            labs = '\n' + ''.join(self._bctx) + '  |-'

            text_list = textwrap.wrap(value, 40)
            labs += '-> {text}'.format(text=text_list[0])
            for text in text_list[1:]:
                labs += '\n' + ''.join(self._bctx) + '       {text}'.format(text=text)
        file.write(labs)

    def _append_bytes(self, value, file):  # pylint: disable=inconsistent-return-statements
        """Call this function to write bytes contents.

        Keyword arguments:
            * value - bytes, content to be dumped
            * file - FileIO, output file

        """
        if not value:
            file.write(' ')
            return self._append_none(None, file)

        value_hex = hexlify(value)
        if len(value_hex) <= 32:
            text = ' '.join(textwrap.wrap(value_hex, 2))
            labs = '-> {text}'.format(text=text)
        else:
            labs = '\n' + ''.join(self._bctx) + '  |-'

            text_list = textwrap.wrap(value_hex, 32)
            text = ' '.join(textwrap.wrap(text_list[0], 2))
            labs += '-> {text}'.format(text=text)
            for item in text_list[1:]:
                text = ' '.join(textwrap.wrap(item, 2))
                labs += '\n' + ''.join(self._bctx) + '       {text}'.format(text=text)
        file.write(labs)

    def _append_date(self, value, file):  # pylint: disable=no-self-use
        """Call this function to write date contents.

        Keyword arguments:
            * value - Union[datetime, date, time], content to be dumped
            * file - FileIO, output file

        """
        text = isoformat(value)
        labs = '-> {text}'.format(text=text)
        file.write(labs)

    def _append_number(self, value, file):  # pylint: disable=no-self-use
        """Call this function to write number contents.

        Keyword arguments:
            * value - Union[int, float, complex], content to be dumped
            * file - FileIO, output file

        """
        if math.isnan(value):
            text = str_type(value).replace(u'nan', u'NaN')
        elif math.isinf(value):
            text = str_type(value).replace(u'inf', u'Infinity')
        else:
            text = value
        labs = '-> {text}'.format(text=text)
        file.write(labs)

    def _append_bool(self, value, file):  # pylint: disable=no-self-use
        """Call this function to write bool contents.

        Keyword arguments:
            * value - bool, content to be dumped
            * file - FileIO, output file

        """
        text = 'True' if value else 'False'
        labs = '-> {text}'.format(text=text)
        file.write(labs)

    def _append_none(self, value, file):  # pylint: disable=unused-argument,no-self-use
        """Call this function to write none contents.

        Keyword arguments:
            * value - NoneType, content to be dumped
            * file - FileIO, output file

        """
        text = 'NIL'
        labs = '-> {text}'.format(text=text)
        file.write(labs)
