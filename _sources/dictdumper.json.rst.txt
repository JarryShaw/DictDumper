JSON Dumper
===========

.. module:: dictdumper.json

:mod:`dictdumper.json` contains :class:`~dictdumper.json.JSON`
only, which dumpers a JavaScript object notation (JSON) file.
Usage sample is described as below.

.. code:: python

   >>> dumper = JSON(file_name)
   >>> dumper(content_dict_1, name=content_name_1)
   >>> dumper(content_dict_2, name=content_name_2)
   ............

Dumper class
------------

.. autoclass:: dictdumper.json.JSON
   :members:
   :undoc-members:
   :show-inheritance:

   .. autoattribute:: dictdumper.json.JSON.__type__
   .. autoattribute:: dictdumper.json.JSON._tctr

      Tab level counter.

      :type: :obj:`int`

   .. autoattribute:: dictdumper.json.JSON._hsrt
   .. autoattribute:: dictdumper.json.JSON._hend

   .. attribute:: _vctr
      :value: defaultdict(<class 'int'>, {})

      Value counter dict.

      :type: :obj:`DefaultDict[int, int]`

Internal utilities
------------------

.. autodata:: dictdumper.json._HEADER_START
.. autodata:: dictdumper.json._HEADER_END
