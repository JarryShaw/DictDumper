# -*- coding: utf-8 -*-
"""base dumper

``dictdumper.dumper`` contains ``Dumper`` only, which is an
abstract base class for all dumpers, eg. HTML, JSON, PLIST,
Tree, and XML.

"""
import abc
import datetime
import functools
import os
import warnings
import sys


# Abstract Base Class of Dumpers
# Pre-define useful arguments and methods of dumpers


__all__ = ['Dumper']


ABCMeta = abc.ABCMeta
abstractmethod = abc.abstractmethod
abstractproperty = abc.abstractproperty


def deprecation(func):
    @functools.wraps(func)
    def wrapper(cls, *args, **kargs):
        if cls.__name__ in ('Dumper', 'JavaScript', 'XML'):
            warnings.warn('%s is deprecated' % cls.__name__, DeprecationWarning, stacklevel=2)
        return func(cls, *args, **kargs)
    return wrapper


class Dumper(object):
    """Abstract base class of all dumpers.

    Usage:
        >>> dumper = Dumper(file_name)
        >>> dumper(content_dict_1, name=content_name_1)
        >>> dumper(content_dict_2, name=content_name_2)
        ............

    Properties:
        * kind - str, file format of current dumper

    Utilities:
        * _dump_header - initially dump file heads and tails
        * _append_value - call this function to write contents

    Attributes:
        * _file - FileIO, output file
        * _sptr - int (file pointer), indicates start of appending point
        * _tctr - int, tab level counter
        * _hrst - str, _HEADER_START
        * _hend - str, _HEADER_END

    """
    __metaclass__ = ABCMeta

    ##########################################################################
    # Attributes.
    ##########################################################################

    _sptr = os.SEEK_SET    # seek pointer
    _tctr = 1              # counter for tab level

    ##########################################################################
    # Properties.
    ##########################################################################

    # file format of current dumper
    @abstractproperty
    def kind(self):
        """File format of current dumper."""
        pass

    ##########################################################################
    # Data models.
    ##########################################################################

    # Not hashable
    __hash__ = None

    @deprecation
    def __new__(cls, fname, **kwargs):
        self = super().__new__(cls)
        self.object_hook = \
            kwargs.get('object_hook', cls.object_hook)
        return self

    def __init__(self, fname, **kwargs):
        if not os.path.isfile(fname):
            open(fname, 'w+').close()
        self._file = fname          # dump file name
        self._dump_header()         # initialise output file

    def __call__(self, value, *, name=None):
        with open(self._file, 'r+') as _file:
            self._append_value(value, _file, name)
            self._sptr = _file.tell()
            _file.write(self._hend)

    ##########################################################################
    # Utilities.
    ##########################################################################

    @classmethod
    def object_hook(cls, obj):
        """Check content type for function call."""
        if isinstance(obj, cls.__type__):
            return obj
        return repr(obj)

    def _dump_header(self):
        """Initially dump file heads and tails."""
        with open(self._file, 'w') as _file:
            _file.write(self._hsrt)
            self._sptr = _file.tell()
            _file.write(self._hend)

    @abstractmethod
    def _append_value(self, value, _file, _name):
        """Call this function to write contents.

        Keyword arguments:
            * value - dict, content to be dunped
            * _file - FileIO, output file
            * _name - str, name of current content dict

        """
        pass
