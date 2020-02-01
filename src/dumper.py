# -*- coding: utf-8 -*-
"""base dumper

``dictdumper.dumper`` contains ``Dumper`` only, which is an
abstract base class for all dumpers, eg. HTML, JSON, PLIST,
Tree, and XML.

"""
# Abstract Base Class of Dumpers
# Pre-define useful arguments and methods of dumpers

import abc
import collections
import os
import warnings

from dictdumper._types import str_type

__all__ = ['Dumper']


def deprecated(cls):
    """Deprecation warning."""
    warnings.warn('%s is deprecated' % cls.__name__, DeprecationWarning, stacklevel=2)
    return cls


class DumperError(TypeError):
    """Unsupported content type."""


class Dumper(object):  # pylint: disable=metaclass-assignment,useless-object-inheritance
    """Abstract base class of all dumpers.

    Usage:
        >>> dumper = Dumper(file_name)
        >>> dumper(content_dict_1, name=content_name_1)
        >>> dumper(content_dict_2, name=content_name_2)
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
        * _hsrt - str, _HEADER_START
        * _hend - str, _HEADER_END

    Utilities:
        * _dump_header - initially dump file heads and tails
        * _encode_func - check content type for function call
        * _encode_value - convert content for function call
        * _append_value - call this function to write contents

    """
    __metaclass__ = abc.ABCMeta

    ##########################################################################
    # Properties.
    ##########################################################################

    # file format of current dumper
    @property
    @abc.abstractmethod
    def kind(self):
        """File format of current dumper."""

    @property
    def filename(self):
        """Output file name."""
        return self._file

    ##########################################################################
    # Type codes.
    ##########################################################################

    __type__ = tuple()

    ##########################################################################
    # Methods.
    ##########################################################################

    @staticmethod
    def make_object(o, value, **kwargs):
        """Create an object with convertion information."""
        obj = collections.OrderedDict()
        obj['type'] = str_type(type(o).__name__)
        obj['value'] = value
        for key, val in kwargs.items():
            obj[key] = val
        return obj

    def object_hook(self, o):  # pylint: disable=unused-argument,no-self-use
        """Convert content for function call."""
        return o

    def default(self, o):  # pylint: disable=unused-argument,no-self-use
        """Check content type for function call."""
        raise DumperError('unsupported content type: %s' % type(o).__name__)

    ##########################################################################
    # Attributes.
    ##########################################################################

    _sptr = os.SEEK_SET    # seek pointer
    _tctr = 1              # counter for tab level

    _hsrt = ''
    _hend = ''

    ##########################################################################
    # Data models.
    ##########################################################################

    def __new__(cls, fname, **kwargs):  # pylint: disable=unused-argument
        self = super(Dumper, cls).__new__(cls)
        return self

    def __init__(self, fname, **kwargs):  # pylint: disable=unused-argument
        self._file = fname          # dump file name
        self._dump_header()         # initialise output file

    def __call__(self, value, name=None):
        with open(self._file, 'r+') as file:
            self._append_value(value, file, name)
            self._sptr = file.tell()
            file.write(self._hend)
        return self

    ##########################################################################
    # Utilities.
    ##########################################################################

    def _dump_header(self):
        """Initially dump file heads and tails."""
        with open(self._file, 'w') as file:
            file.write(self._hsrt)
            self._sptr = file.tell()
            file.write(self._hend)

    def _encode_func(self, o):
        """Check content type for function call."""
        name = None
        for (kind, code) in self.__type__:
            if isinstance(o, kind):
                name = code
                break
        if name is None:
            name = self.default(o)  # pylint: disable=assignment-from-no-return

        func = '_append_%s' % name
        return getattr(self, func)

    def _encode_value(self, o):
        """Convert content for function call."""
        return self.object_hook(o)

    @abc.abstractmethod
    def _append_value(self, value, file, name):
        """Call this function to write contents.

        Keyword arguments:
            * value - dict, content to be dumped
            * file - FileIO, output file
            * name - str, name of current content dict

        """
