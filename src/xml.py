# -*- coding: utf-8 -*-
"""dumper a XML file (DEPRECATED)

    Note that this file is deprecated.

``dictdumper.xml`` contains ``XML`` only, which dumpers an
extensible markup language (XML) format file. However, due
to lack of supported ``dtd``, the output file is currently
meaningless, thus it is now deprecated. Usage sample is
described as below.

    >>> dumper = XML(file_name)
    >>> dumper(content_dict_1, name=content_name_1)
    >>> dumper(content_dict_2, name=content_name_2)
    ............

"""
# TODO: Supports more `dtd`s of XML.


import os
import textwrap


# Dumper for XML files
# Write a XML file for PCAP analyser


from dictdumper.dumper import Dumper


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
        * kind - str, return 'plist'

    Methods:
        * object_hook - default/customised object hooks

    Attributes:
        * _file - FileIO, output file
        * _sptr - int (file pointer), indicates start of appending point
        * _tctr - int, tab level counter
        * _hrst - str, _HEADER_START
        * _hend - str, _HEADER_END

    Methods:
        * _dump_header - initially dump file heads and tails
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
