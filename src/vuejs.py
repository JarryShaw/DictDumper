# -*- coding: utf-8 -*-
"""dumper a Vue.js file (DEPRECATED)

    Note that this file is deprecated.

``dictdumper.js`` contains ``JavaScript`` only, which dumpers
a JavaScript file using the ``Vue.js`` framework. However,
due to errors in grammar, the output file won't work, thus
it is now deprecated. Usage sample is described as below.

    >>> dumper = VueJS(file_name)
    >>> dumper(content_dict_1, name=content_name_1)
    >>> dumper(content_dict_2, name=content_name_2)
    ............

"""
# Writer for Vue.js files
# Dump a Vue.js file for PCAP analyser

from dictdumper.dumper import deprecated
from dictdumper.json import JSON

__all__ = ['VueJS']

# head
_HEADER_START = '''\
// demo data
var data = {\n
'''

# tail
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

    Usage:
        >>> dumper = VueJS(file_name)
        >>> dumper(content_dict_1, name=content_name_1)
        >>> dumper(content_dict_2, name=content_name_2)
        ............

    Properties:
        * kind - str, file format of current dumper
        * filename - str, output file name

    Methods:
        * make_object - create an object with convertion information
        * object_hook - convert content for function call
        * default - check content type for function call

    Attributes:
        * _file - str, output file name
        * _sptr - int (file pointer), indicates start of appending point
        * _tctr - int, tab level counter
        * _hrst - str, _HEADER_START
        * _hend - str, _HEADER_END
        * _vctr - dict, value counter dict

    Utilities:
        * _dump_header - initially dump file heads and tails
        * _encode_func - check content type for function call
        * _encode_value - convert content for function call
        * _append_value - call this function to write contents

    """
    ##########################################################################
    # Properties.
    ##########################################################################

    @property
    def kind(self):
        """File format of current dumper."""
        return 'js'

    ##########################################################################
    # Attributes.
    ##########################################################################

    _hsrt = _HEADER_START
    _hend = _HEADER_END
