PLIST Dumper
============

.. module:: dictdumper.plist

:mod:`dictdumper.plist` contains :class:`~dictdumper.plist.PLIST`
only, which dumpers an Apple property list (PLIST) file. Usage
sample is described as below.

Dumper class
------------

.. autoclass:: dictdumper.plist.PLIST
   :members:
   :undoc-members:
   :show-inheritance:

   .. autoattribute:: dictdumper.plist.PLIST.__type__
   .. autoattribute:: dictdumper.plist.PLIST._tctr

      Tab level counter.

      :type: :obj:`int`

   .. autoattribute:: dictdumper.plist.PLIST._hsrt
   .. autoattribute:: dictdumper.plist.PLIST._hend

Internal utilities
------------------

.. autodata:: dictdumper.plist._HEADER_START
.. autodata:: dictdumper.plist._HEADER_END
