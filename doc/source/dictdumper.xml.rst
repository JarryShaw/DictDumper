Base XML Dumper
===============

.. module:: dictdumper.xml

.. note::

    Do not use the :class:`~dictdumper.xml.XML` directly.

:mod:`dictdumper.xml` contains :class:`~dictdumper.xml.XML`
only, which dumpers an extensible markup language (XML) format
file. Usage sample is described as below.

.. code:: python

   >>> dumper = XML(file_name)
   >>> dumper(content_dict_1, name=content_name_1)
   >>> dumper(content_dict_2, name=content_name_2)
   ............

.. todo::

    * Supports more ``dtd`` of XML.

Dumper class
------------

.. autoclass:: dictdumper.xml.XML
   :members:
   :undoc-members:
   :show-inheritance:

   .. autoattribute:: dictdumper.xml.XML.__type__

      Type codes.

      :type: :obj:`Tuple[Tuple[type, str]]`

   .. autoattribute:: dictdumper.xml.XML._tctr

      Tab level counter.

      :type: :obj:`int`

   .. autoattribute:: dictdumper.xml.XML._hsrt
   .. autoattribute:: dictdumper.xml.XML._hend

Internal utilities
------------------

.. autodata:: dictdumper.xml._HEADER_START
.. autodata:: dictdumper.xml._HEADER_END
