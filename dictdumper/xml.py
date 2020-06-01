# -*- coding: utf-8 -*-
"""dumper a XML file

.. note::

    Do not use the :class:`~dictdumper.xml.XML` directly.

:mod:`dictdumper.xml` contains :class:`~dictdumper.xml.XML`
only, which dumpers an extensible markup language (XML) format
file. Usage sample is described as below.

.. code:: python

    >>> dumper = XML(file_name)
    >>> dumper(content_dict_1, name=content_name_1)
    >>> dumper(content_dict_2, name=content_name_2)
    ............

.. todo::

    * Supports more ``dtd`` of XML.

"""
# TODO: Supports more ``dtd`` of XML.  # pylint: disable=fixme

# Dumper for XML files
# Write a XML file for PCAP analyser

import abc

from dictdumper.dumper import Dumper

__all__ = ['XML']

#: XML head string.
_HEADER_START = '''\
<?xml version="1.0" encoding="UTF-8"?>
<content>
'''

#: XML tail string.
_HEADER_END = '''\
</content>
'''


class XML(Dumper):
    """Dump extensible markup language (XML) file.

    Note:
        This is a base dumper for XML format. No ``dtd`` supported.

    .. code:: python

        >>> dumper = XML(file_name)
        >>> dumper(content_dict_1, name=content_name_1)
        >>> dumper(content_dict_2, name=content_name_2)
        ............

    Attributes:
        _file (str): output file name
        _sptr (int): indicates start of appending point (file pointer)
        _tctr (int): tab level counter
        _hsrt (str): start string (:data:`~dictdumper.plist._HEADER_START`)
        _hend (str): end string (:data:`~dictdumper.plist._HEADER_END`)

    """
    ##########################################################################
    # Properties.
    ##########################################################################

    @property
    def kind(self):
        """File format of current dumper.

        :rtype: Literal['xml']
        """
        return 'xml'

    ##########################################################################
    # Attributes.
    ##########################################################################

    #: XML head string.
    _hsrt = _HEADER_START
    #: XML tail string.
    _hend = _HEADER_END

    ##########################################################################
    # Utilities.
    ##########################################################################

    @abc.abstractmethod
    def _append_value(self, value, file, name):
        """Call this function to write contents.

        Args:
            value (Dict[str, Any]): content to be dumped
            file (io.TextIOWrapper): output file
            name (str): name of current content block

        """
