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
        dump extensible markup language (``XML``) file;
        this is a abstract base class

-  ``dictdumper.VueJS``
        dump JavaScript file using ``Vue.js`` framework;
        this class is deprecated due to grammar error

"""
# Base Class for DictDumper
from dictdumper.dumper import Dumper  # pylint: disable=unused-import
from dictdumper.xml import XML  # pylint: disable=unused-import

# Utility Classes
from dictdumper.json import JSON
from dictdumper.plist import PLIST
from dictdumper.tree import Tree

# Deprecated Classes
from dictdumper.vuejs import VueJS  # pylint: disable=unused-import

__all__ = ['JSON', 'PLIST', 'Tree']
