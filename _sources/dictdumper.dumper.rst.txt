Base Dumper
===========

.. module:: dictdumper.dumpers

:mod:`~dictdumper.dumper` contains :class:`~dictdumper.dumper.Dumper` only,
which is an abstract base class for all dumpers, eg. :class:`~dictdumper.vuejs.VueJS`,
:class:`~dictdumper.json.JSON`, :class:`~dictdumper.plist.PLIST`,
:class:`~dictdumper.tree.Tree`, and :class:`~dictdumper.xml.XML`.

Dumper class
------------

.. autoclass:: dictdumper.dumper.Dumper
   :members:
   :undoc-members:
   :show-inheritance:

   .. autoattribute:: dictdumper.dumper.Dumper.__type__
   .. autoattribute:: dictdumper.dumper.Dumper._tctr

   .. autoattribute:: dictdumper.dumper.Dumper._hsrt
   .. autoattribute:: dictdumper.dumper.Dumper._hend

Internal utilities
------------------

.. autofunction:: dictdumper.dumper.deprecated

.. autoexception:: dictdumper.dumper.DumperError
   :members:
   :undoc-members:
   :show-inheritance:
