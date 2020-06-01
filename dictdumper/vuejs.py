# -*- coding: utf-8 -*-
"""dumper a Vue.js file (DEPRECATED)

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

"""
# Writer for Vue.js files
# Dump a Vue.js file for PCAP analyser

from dictdumper.dumper import deprecated
from dictdumper.json import JSON

__all__ = ['VueJS']

#: Vue.js head string.
_HEADER_START = '''\
// demo data
var data = {\n
'''

#: Vue.js tail string.
_HEADER_END = """
\n}

// define the item component
Vue.component('item', {
  template: '#item-template',
  props: {
    model: Object
  },
  data: function () {
    return {
      open: false
    }
  },
  computed: {
    isFolder: function () {
      return this.model.children &&
        this.model.children.length
    }
  },
  methods: {
    toggle: function () {
      if (this.isFolder) {
        this.open = !this.open
      }
    },
    changeType: function () {
      if (!this.isFolder) {
        Vue.set(this.model, 'children', [])
        this.addChild()
        this.open = true
      }
    },
    addChild: function () {
      this.model.children.push({
        name: 'new stuff'
      })
    }
  }
})

// boot up the demo
var demo = new Vue({
  el: '#demo',
  data: {
    treeData: data
  }
})
"""


@deprecated
class VueJS(JSON):
    """Dump JavaScript file using `Vue.js` framework.

    .. code:: python

        >>> dumper = VueJS(file_name)
        >>> dumper(content_dict_1, name=content_name_1)
        >>> dumper(content_dict_2, name=content_name_2)
        ............

    Attributes:
        _file (str): output file name
        _sptr (int): indicates start of appending point (file pointer)
        _tctr (int): tab level counter
        _hsrt (str): :data:`~dictdumper.json._HEADER_START`
        _hend (str): :data:`~dictdumper.json._HEADER_END`
        _vctr (DefaultDict[int, int]): value counter dict

    """
    ##########################################################################
    # Properties.
    ##########################################################################

    @property
    def kind(self):
        """File format of current dumper.

        :rtype: Literal['js']
        """
        return 'js'

    ##########################################################################
    # Attributes.
    ##########################################################################

    #: Vue.js head string.
    _hsrt = _HEADER_START
    #: Vue.js tail string.
    _hend = _HEADER_END
