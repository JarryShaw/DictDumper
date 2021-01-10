Tree-View Dumper
================

.. module:: dictdumper.tree

:mod:`dictdumper.tree` contains :class:`~dictdumper.tree.Tree`
only, which dumpers a tree-view text (TXT) format file. Usage
sample is described as below.

.. code:: python

    >>> dumper = Tree(filename)
    >>> dumper(content_dict_1, name=contentname_1)
    >>> dumper(content_dict_2, name=contentname_2)
    ............

Dumper class
------------

.. autoclass:: dictdumper.tree.Tree
   :members:
   :undoc-members:
   :show-inheritance:

   .. autoattribute:: dictdumper.tree.Tree.__type__
   .. autoattribute:: dictdumper.tree.Tree._tctr

      Tab level counter.

      :type: :obj:`int`

   .. autoattribute:: dictdumper.tree.Tree._hsrt
   .. autoattribute:: dictdumper.tree.Tree._hend

   .. autoattribute:: dictdumper.tree.Tree._nctr
   .. autoattribute:: dictdumper.tree.Tree._bctx

Internal utilities
------------------

.. autofunction:: dictdumper.tree.indent

.. autodata:: dictdumper.tree._HEADER_START
.. autodata:: dictdumper.tree._HEADER_END

.. autodata:: dictdumper.tree._TEMP_BRANCH
.. autodata:: dictdumper.tree._TEMP_SPACES
