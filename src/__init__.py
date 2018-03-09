# -*- coding: utf-8 -*-
"""stream formatted output dumper

``jsformat`` is an open source Python program works as a
stream formatted output dumper. Currently, it supports
following formats --

-  ``jsformat.Dumper``
        abstract base class of all dumpers

-  ``jsformat.JSON``
        dump JavaScript object notation (``JSON``)
        format file

-  ``jsformat.PLIST``
        dump Apple property list (``PLIST``) format file

-  ``jsformat.Tree``
        dump tree-view text (``TXT``) format file

-  ``jsformat.XML``
        dump extensible Mmarkup language (``XML``) file;
        this is a deprecated base class

-  ``jsformat.HTML``
        dump JavaScript file under ``Vue.js`` framework
        this class is deprecated due to grammar error

"""
# Base Class for jsFormat
from jsformat.dumper import Dumper

# Utility Classes
from jsformat.json import JSON
from jsformat.plist import PLIST
from jsformat.tree import Tree

# Deprecated / Base Classes
from jsformat.html import JavaScript
from jsformat.xml import XML


__all__ = ['JSON', 'PLIST', 'Tree']
