# -*- coding: utf-8 -*-
"""dumper a XML file (DEPRECATED)

    Note that this file is deprecated.

``dictdumper.xml`` contains ``XML`` only, which dumpers an
extensible markup language (XML) format file. Usage sample
is described as below.

    >>> dumper = XML(file_name)
    >>> dumper(content_dict_1, name=content_name_1)
    >>> dumper(content_dict_2, name=content_name_2)
    ............

"""
# TODO: Supports more `dtd`s of XML.  # pylint: disable=fixme

# Dumper for XML files
# Write a XML file for PCAP analyser

import abc

from dictdumper.dumper import Dumper

__all__ = ['XML']

# head
_HEADER_START = '''\
<?xml version="1.0" encoding="UTF-8"?>
<content>
'''

# tail
_HEADER_END = '''\
</content>
'''


class XML(Dumper):
    """Dump extensible markup language (XML) file.

    Note:
        This is a base dumper for XML format. No `dtd` supported.

    Usage:
        >>> dumper = XML(file_name)
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
        * _hrst - str, _HEADER_START
        * _hend - str, _HEADER_END

    Utilities:
        * _dump_header - initially dump file heads and tails
        * _encode_func - check content type for function call
        * _encode_value - convert content for function call
        * _append_value - call this function to write contents

    """
    ##########################################################################
    # Properties.
    ##########################################################################

    @property
    def kind(self):
        """File format of current dumper."""
        return 'xml'

    ##########################################################################
    # Attributes.
    ##########################################################################

    _hsrt = _HEADER_START
    _hend = _HEADER_END

    ##########################################################################
    # Utilities.
    ##########################################################################

    @abc.abstractmethod
    def _append_value(self, value, _file, _name):
        pass
