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
# Writer for JSON files
# Dump a JSON file for PCAP analyser

from __future__ import unicode_literals

import collections
import datetime
import math
import os

from dictdumper._dateutil import isoformat
from dictdumper._hexlify import hexlify
from dictdumper._types import bytes_type, str_type
from dictdumper.dumper import Dumper

__all__ = ['JSON']

# head
_HEADER_START = '{\n'

# tail
_HEADER_END = '\n}'


class JSON(Dumper):
    """Dump JavaScript object notation (JSON) format file.

    Usage:
        >>> dumper = JSON(file_name)
        >>> dumper(content_dict_1, name=content_name_1)
        >>> dumper(content_dict_2, name=content_name_2)
        ............

    Properties:
        * kind - str, return 'json'
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
        * _vctr - dict, value counter dict

    Utilities:
        * _dump_header - initially dump file heads and tails
        * _encode_func - check content type for function call
        * _encode_value - convert content for function call
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
        # string
        (str_type, 'string'),

        # date
        (datetime.date, 'date'),
        (datetime.datetime, 'date'),
        (datetime.time, 'date'),

        # bool
        (bool, 'bool'),

        # number
        (int, 'number'),
        (float, 'number'),

        # object
        (dict, 'object'),

        # array
        (list, 'array'),

        # null
        (type(None), 'null'),
    )

    ##########################################################################
    # Attributes.
    ##########################################################################

    _hsrt = _HEADER_START
    _hend = _HEADER_END

    ##########################################################################
    # Data models.
    ##########################################################################

    def __init__(self, fname, **kwargs):
        super(JSON, self).__init__(fname, **kwargs)

        self._vctr = collections.defaultdict(int)  # value counter dict

    ##########################################################################
    # Utilities.
    ##########################################################################

    def _encode_value(self, o):  # pylint: disable=unused-argument
        """Convert content for function call."""
        if isinstance(o, (bytes_type, bytearray)):
            return self.make_object(o, o.decode(errors='replace'), hex=hexlify(o))
        if isinstance(o, memoryview):
            tobytes = o.tobytes()
            return self.make_object(o, tobytes.decode(errors='replace'), hex=hexlify(tobytes))
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
        tabs = '\t' * self._tctr
        cmma = ',\n' if self._vctr[self._tctr] else ''
        keys = '{cmma}{tabs}"{name}": '.format(cmma=cmma, tabs=tabs, name=name)

        file.seek(self._sptr, os.SEEK_SET)
        file.write(keys)

        self._vctr[self._tctr] += 1
        self._append_object(value, file)

    ##########################################################################
    # Functions.
    ##########################################################################

    def _append_object(self, value, file):
        """Call this function to write object contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * file - FileIO, output file

        """
        labs = '{'
        file.write(labs)
        self._tctr += 1

        for (item, text) in value.items():
            tabs = '\t' * self._tctr
            cmma = ',' if self._vctr[self._tctr] else ''
            keys = '{cmma}\n{tabs}"{item}": '.format(cmma=cmma, tabs=tabs, item=item)
            file.write(keys)

            self._vctr[self._tctr] += 1

            enc_text = self._encode_value(text)
            func = self._encode_func(enc_text)
            func(enc_text, file)

        self._vctr[self._tctr] = 0
        self._tctr -= 1
        tabs = '\t' * self._tctr
        labs = '\n{tabs}{}'.format('}', tabs=tabs)
        file.write(labs)

    def _append_array(self, value, file):
        """Call this function to write array contents.

        Keyword arguments:
            * value - list, content to be dumped
            * file - FileIO, output file

        """
        val_list = [self._encode_value(item) for item in value]
        mul_line = False
        for item in val_list:
            if isinstance(item, dict):
                mul_line = True
                break

        labs = '[\n' if mul_line else '[ '
        file.write(labs)

        self._tctr += 1

        tabs = '\t' * self._tctr
        for item in val_list:
            if self._vctr[self._tctr]:
                file.write(',\n' if mul_line else ', ')
            if mul_line:
                file.write(tabs)

            self._vctr[self._tctr] += 1

            func = self._encode_func(item)
            func(item, file)

        self._vctr[self._tctr] = 0
        self._tctr -= 1

        if mul_line:
            tabs = '\t' * self._tctr
            labs = '\n{tabs}]'.format(tabs=tabs)
        else:
            labs = ' ]'
        file.write(labs)

    def _append_string(self, value, file):  # pylint: disable=no-self-use
        """Call this function to write string contents.

        Keyword arguments:
            * value - str, content to be dumped
            * file - FileIO, output file

        """
        text = str_type(value).replace(u'"', u'\\"')
        labs = '"{text}"'.format(text=text)
        file.write(labs)

    def _append_date(self, value, file):  # pylint: disable=no-self-use
        """Call this function to write date contents.

        Keyword arguments:
            * value - Union[date, datetime, time], content to be dumped
            * file - FileIO, output file

        """
        text = isoformat(value)
        labs = '"{text}"'.format(text=text)
        file.write(labs)

    def _append_number(self, value, file):
        """Call this function to write number contents.

        Keyword arguments:
            * value - Union[int, float], content to be dumped
            * file - FileIO, output file

        """
        if math.isnan(value):
            text = self.make_object(value, None, number=str_type(value).replace(u'nan', u'NaN'))
            self._append_object(text, file)
        elif math.isinf(value):
            text = self.make_object(value, None, number=str_type(value).replace(u'inf', u'Infinity'))
            self._append_object(text, file)
        else:
            labs = str_type(value)
            file.write(labs)

    def _append_bool(self, value, file):  # pylint: disable=no-self-use
        """Call this function to write bool contents.

        Keyword arguments:
            * value - bool, content to be dumped
            * file - FileIO, output file

        """
        labs = 'true' if value else 'false'
        file.write(labs)

    def _append_null(self, value, file):  # pylint: disable=unused-argument,no-self-use
        """Call this function to write null contents.

        Keyword arguments:
            * value - NoneType, content to be dumped
            * file - FileIO, output file

        """
        labs = 'null'
        file.write(labs)
