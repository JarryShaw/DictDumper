# -*- coding: utf-8 -*-
"""stream formatted output dumper

``dictdumper`` is an open source Python program works as a
stream formatted output dumper. Currently, it supports
following formats --

-  ``dictdumper.Dumper``
        abstract base class of all dumpers

-  ``dictdumper.JSON``
        dump JavaScript object notation (``JSON``)
        format file

-  ``dictdumper.PLIST``
        dump Apple property list (``PLIST``) format file

-  ``dictdumper.Tree``
        dump tree-view text (``TXT``) format file

-  ``dictdumper.XML``
        dump extensible Mmarkup language (``XML``) file;
        this is a deprecated base class

-  ``dictdumper.HTML``
        dump JavaScript file under ``Vue.js`` framework
        this class is deprecated due to grammar error

"""
# Base Class for jsFormat
from dictdumper.dumper import Dumper

# Utility Classes
from dictdumper.json import JSON
from dictdumper.plist import PLIST
from dictdumper.tree import Tree

# Deprecated / Base Classes
from dictdumper.html import JavaScript
from dictdumper.xml import XML


__all__ = ['JSON', 'PLIST', 'Tree']
