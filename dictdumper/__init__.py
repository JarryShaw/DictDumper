# -*- coding: utf-8 -*-
"""Stream formatted output dumper.

:mod:`dictdumper` is an open source Python program works as a
stream formatted output dumper. Currently, it supports
following formats:

- :class:`~dictdumper.dumper.Dumper`

  Abstract base class of all dumpers.

- :class:`~dictdumper.json.JSON`

  Dump JavaScript object notation (``JSON``) format file.

- :class:`~dictdumper.plist.PLIST`

  Dump Apple property list (``PLIST``) format file.

- :class:`~dictdumper.tree.Tree`

  Dump tree-view text (``TXT``) format file.

- :class:`~dictdumper.xml.XML`

  Dump extensible markup language (``XML``) file;
  this is an abstract base class

- :class:`~dictdumper.vuejs.VueJS`

  Dump JavaScript file using ``Vue.js`` framework;
  this class is deprecated due to grammar error.

  .. deprecated:: 0.8.0

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
