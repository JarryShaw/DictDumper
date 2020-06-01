# -*- coding: utf-8 -*-
"""dumper a tree-view file

:mod:`dictdumper.plist` contains :class:`~dictdumper.tree.Tree`
only, which dumpers a tree-view text (TXT) format file. Usage
sample is described as below.

.. code:: python

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

try:
    from contextlib import nullcontext
except ImportError:
    class nullcontext:
        """Context manager that does no additional processing."""

        def __enter__(self):
            return self

        def __exit__(self, *excinfo):
            pass

# headers
#: Tree-view head string.
_HEADER_START = ''  # head
#: Tree-view tail string.
_HEADER_END = ''    # tail

# templates
#: Branch template
_TEMP_BRANCH = '  |   '  # branch
#: Spaces template
_TEMP_SPACES = '      '  # spaces


@contextlib.contextmanager
def indent(ctx, branch=True):
    """Indentation context.

    Args:
        ctx (:obj:`List[str]`): indentation context
        branch (bool): if ``True`` push the branch template
            (:data:`~dictdumper.tree._TEMP_BRANCH`) to the context, else push
            the spaces template (:data:`~dictdumper.tree._TEMP_SPACES`)

    Yields:
        ``None``: temporarily push a template to the context

    """
    if branch:
        ctx.append(_TEMP_BRANCH)
    else:
        ctx.append(_TEMP_SPACES)
    yield
    ctx.pop()


class Tree(Dumper):
    """Dump a tree-view text (TXT) format file.

    .. code:: python

        >>> dumper = Tree(filename)
        >>> dumper(content_dict_1, name=contentname_1)
        >>> dumper(content_dict_2, name=contentname_2)
        ............


    Attributes:
        _file (str): output file name
        _sptr (int): indicates start of appending point (file pointer)
        _tctr (int): tab level counter
        _hsrt (str): start string (:data:`~dictdumper.tree._HEADER_START`)
        _hend (str): end string (:data:`~dictdumper.tree._HEADER_END`)
        _bctx (List[str]): blank branch (indentation) context record
        _nctr (int): branch number counter

    .. note::

        Terminology:

        .. code::

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
        """File format of current dumper.

        :rtype: Literal['txt']
        """
        return 'txt'

    ##########################################################################
    # Type codes.
    ##########################################################################

    #: Tuple[Tuple[type, str]]: Type codes.
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
        """Check if newline is needed.

        Args:
            value (Union[Dict[str, Any], AnyStr]): value to check if
                new line is needed

        Returns:
            bool: if newline is needed

        Notes:
            Newline is needed if

            1. ``value`` is a :obj:`dict`
            2. ``value`` is string (:obj:`str`) and its length is greater than
               32 distinct characters
            3. ``value`` is bytestring (:obj:`bytes`) and the length of its hex
               representation is greater than 40 distinct characters

        """
        if isinstance(value, dict):
            return True
        if isinstance(value, str_type):
            return len(value) > 40
        if isinstance(value, bytes_type):
            return len(hexlify(value)) > 32
        return False

    ##########################################################################
    # Attributes.
    ##########################################################################

    #: int: Branch number counter.
    _nctr = 0
    #: List[str]: Blank branch (indentation) context record.
    _bctx = list()

    #: Tree-view head string.
    _hsrt = _HEADER_START
    #: Tree-view tail string.
    _hend = _HEADER_END

    ##########################################################################
    # Utilities.
    ##########################################################################

    def _encode_value(self, o):  # pylint: disable=unused-argument
        """Convert content for function call.

        Args:
            o (Any): object to convert

        Returns:
            Any: the converted object

        See Also:
            The function is a direct wrapper for :meth:`~dictdumper.dumper.Dumper.object_hook`.

        Notes:
            The function will by default converts :obj:`bytearray`,
            :obj:`memoryview`, :obj:`tuple`, :obj:`set`, :obj:`frozenset` to
            tree-view represetable data.

        """
        if isinstance(o, bytearray):
            return self.make_object(o, bytes_type(o), text=o.decode(errors='replace'))
        if isinstance(o, memoryview):
            tobytes = o.tobytes()
            return self.make_object(o, tobytes, text=tobytes.decode(errors='replace'))
        if isinstance(o, (tuple, set, frozenset)):
            return self.make_object(o, list(o))
        return self.object_hook(o)

    def _append_value(self, value, file, name):
        """Call this function to write contents.

        Args:
            value (Dict[str, Any]): content to be dumped
            file (io.TextIOWrapper): output file
            name (str): name of current content block

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

        Args:
            value (Dict[str, Any]): content to be dumped
            file (io.TextIOWrapper): output file

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

        Args:
            value (List[Any]): content to be dumped
            file (io.TextIOWrapper): output file

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

        Args:
            value (str): content to be dumped
            file (io.TextIOWrapper): output file

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

        Args:
            value (bytes): content to be dumped
            file (io.TextIOWrapper): output file

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

        Args:
            value (Union[datetime.date, datetime.datetime, datetime.time]): content to be dumped
            file (io.TextIOWrapper): output file

        """
        text = isoformat(value)
        labs = '-> {text}'.format(text=text)
        file.write(labs)

    def _append_number(self, value, file):  # pylint: disable=no-self-use
        """Call this function to write number contents.

        Args:
            value (Union[int, float, complex]): content to be dumped
            file (io.TextIOWrapper): output file

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

        Args:
            value (bool): content to be dumped
            file (io.TextIOWrapper): output file

        """
        text = 'True' if value else 'False'
        labs = '-> {text}'.format(text=text)
        file.write(labs)

    def _append_none(self, value, file):  # pylint: disable=unused-argument,no-self-use
        """Call this function to write none contents.

        Args:
            value (None): content to be dumped
            file (io.TextIOWrapper): output file

        """
        text = 'NIL'
        labs = '-> {text}'.format(text=text)
        file.write(labs)
