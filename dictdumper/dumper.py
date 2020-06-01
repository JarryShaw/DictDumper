# -*- coding: utf-8 -*-
"""base dumper

:mod:`~dictdumper.dumper` contains :class:`~dictdumper.dumper.Dumper` only,
which is an abstract base class for all dumpers, eg. :class:`~dictdumper.vuejs.VueJS`,
:class:`~dictdumper.json.JSON`, :class:`~dictdumper.plist.PLIST`,
:class:`~dictdumper.tree.Tree`, and :class:`~dictdumper.xml.XML`.

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
    """Deprecation warning.

    Args:
        cls (object): the class to mark as deprecated

    Returns:
        object: The original ``cls`` itself.

    """
    warnings.warn('%s is deprecated' % cls.__name__, DeprecationWarning, stacklevel=2)
    return cls


class DumperError(TypeError):
    """Unsupported content type."""


class Dumper(object):  # pylint: disable=metaclass-assignment,useless-object-inheritance
    """Abstract base class of all dumpers.

    .. code:: python

        >>> dumper = Dumper(file_name)
        >>> dumper(content_dict_1, name=content_name_1)
        >>> dumper(content_dict_2, name=content_name_2)
        ............

    Attributes:
        _file (str): output file name
        _sptr (int): indicates start of appending point (file pointer)
        _tctr (int): tab level counter
        _hsrt (str): start string (``_HEADER_START``)
        _hend (str): end string (``_HEADER_END``)

    """
    __metaclass__ = abc.ABCMeta

    ##########################################################################
    # Properties.
    ##########################################################################

    # file format of current dumper
    @property
    @abc.abstractmethod
    def kind(self):
        """File format of current dumper.

        :rtype: str
        """

    @property
    def filename(self):
        """Output file name.

        :rtype: str
        """
        return self._file

    ##########################################################################
    # Type codes.
    ##########################################################################

    #: Tuple[Tuple[type, str]]: Type codes.
    __type__ = tuple()

    ##########################################################################
    # Methods.
    ##########################################################################

    @staticmethod
    def make_object(o, value, **kwargs):
        """Create an object with convertion information.

        Args:
            o (Any): object to convert
            value (Any): converted value of ``o``
            **kwargs: additional information for the convertion

        Returns:
            Dict[str, Any]: Information context of the convertion.

        """
        obj = collections.OrderedDict()
        obj['type'] = str_type(type(o).__name__)
        obj['value'] = value
        for key, val in kwargs.items():
            obj[key] = val
        return obj

    def object_hook(self, o):  # pylint: disable=unused-argument,no-self-use
        """Convert content for function call.

        Args:
            o (Any): object to convert

        Returns:
            Any: the converted object

        """
        return o

    def default(self, o):  # pylint: disable=unused-argument,no-self-use
        """Check content type for function call.

        Args:
            o (Any): object to check

        Raises:
            DumperError: ``o`` is an unsupported content type

        """
        raise DumperError('unsupported content type: %s' % type(o).__name__)

    ##########################################################################
    # Attributes.
    ##########################################################################

    #: :obj:`int`, file pointer: Indicates start of appending point.
    _sptr = os.SEEK_SET    # seek pointer
    #: :obj:`int`: Tab level counter.
    _tctr = 1              # counter for tab level

    #: Dumper head string.
    _hsrt = ''
    #: Dumper tail string.
    _hend = ''

    ##########################################################################
    # Data models.
    ##########################################################################

    def __new__(cls, fname, **kwargs):  # pylint: disable=unused-argument
        self = super(Dumper, cls).__new__(cls)
        return self

    def __init__(self, fname, **kwargs):  # pylint: disable=unused-argument
        """Initialise dumper.

        Args:
            fname (str): output file name
            **kwargs: addition keyword arguments for initialisation

        """
        self._file = fname           # dump file name
        self._dump_header(**kwargs)  # initialise output file

    def __call__(self, value, name=None):
        """Dumper a new block.

        Args:
            value (Dict[str, Any]): content to be dumped
            name (v): name of current content block

        Returns:
            Dumper: the dumper class itself (to support chain calling)

        """
        with open(self._file, 'r+') as file:
            self._append_value(value, file, name)
            self._sptr = file.tell()
            file.write(self._hend)
        return self

    ##########################################################################
    # Utilities.
    ##########################################################################

    def _dump_header(self, **kwargs):  # pylint: disable=unused-argument
        """Initially dump file heads and tails.

        Keyword Args:
            **kwargs: Arbitrary keyword arguments.

        """
        with open(self._file, 'w') as file:
            file.write(self._hsrt)
            self._sptr = file.tell()
            file.write(self._hend)

    def _encode_func(self, o):
        """Check content type for function call.

        Args:
            o (Any): object to check

        See Also:
            If the type of ``o`` is not defined in :attr:`~Dumper.__type__`,
            the function refers to :meth:`~Dumper.default` for custom hooks.

        """
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
        """Convert content for function call.

        Args:
            o (Any): object to convert

        Returns:
            Any: the converted object

        See Also:
            The function is a direct wrapper for :meth:`~Dumper.object_hook`.

        """
        return self.object_hook(o)

    @abc.abstractmethod
    def _append_value(self, value, file, name):
        """Call this function to write contents.

        Args:
            value (Dict[str, Any]): content to be dumped
            file (io.TextIOWrapper): output file
            name (str): name of current content block

        """
