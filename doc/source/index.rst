.. DictDumper documentation master file, created by
   sphinx-quickstart on Sat Feb 15 12:01:40 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DictDumper - Stream Formatted Output Dumper
===========================================

The :mod:`dictdumper` project is an open source Python program works as a
stream formatted output dumper for :obj:`dict`.

.. toctree::
   :maxdepth: 3

   dictdumper

Currently, the module supports following formats --

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

.. note::

   The :class:`~dictdumper.xml.XML` class is an abstract
   base class for XML format dumpers.

.. warning::

   The :class:`~dictdumper.vuejs.VueJS` class is deprecated
   due to errors in grammar.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
