#!/usr/bin/python3
# -*- coding: utf-8 -*-


# TODO: Supports more `dtd`s of XML.


import os
import textwrap


# Dumper for XML files
# Write a XML file for PCAP analyser


from jsformat.dumper import Dumper


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
    """Dump extensible Mmarkup language (XML) file.

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
        * _dump_header - initially dump file heads and tails
        * _append_value - call this function to write contents

    Attributes:
        * _file - FileIO, output file
        * _sptr - int (file pointer), indicates start of appending point
        * _tctr - int, tab level counter
        * _hrst - str, _HEADER_START
        * _hend - str, _HEADER_END

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
