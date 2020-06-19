Vue.js Dumper (DEPRECATED)
==========================

.. module:: dictdumper.vuejs

.. note::

    Note that this file is deprecated.

:mod:`dictdumper.vuejs` contains :class:`~dictdumper.vuejs.VueJS`
only, which dumpers a JavaScript file using the ``Vue.js`` framework.
However, due to errors in grammar, the output file won't work,
thus it is now deprecated. Usage sample is described as below.

.. code:: python

    >>> dumper = VueJS(file_name)
    >>> dumper(content_dict_1, name=content_name_1)
    >>> dumper(content_dict_2, name=content_name_2)
    ............

.. deprecated:: 0.8.0

Dumper class
------------

.. autoclass:: dictdumper.vuejs.VueJS
   :members:
   :undoc-members:
   :show-inheritance:

   .. autoattribute:: dictdumper.vuejs.VueJS.__type__

      Type codes.

      :type: :obj:`Tuple[Tuple[type, str]]`

   .. autoattribute:: dictdumper.vuejs.VueJS._tctr

      Tab level counter.

      :type: :obj:`int`

   .. autoattribute:: dictdumper.vuejs.VueJS._hsrt
   .. autoattribute:: dictdumper.vuejs.VueJS._hend

   .. attribute:: _vctr
      :value: defaultdict(<class 'int'>, {})

      Value counter dict.

      :type: :obj:`DefaultDict[int, int]`

Internal utilities
------------------

.. autodata:: dictdumper.vuejs._HEADER_START
.. autodata:: dictdumper.vuejs._HEADER_END
