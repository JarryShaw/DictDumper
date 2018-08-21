# -*- coding: utf-8 -*-
"""dumper a JavaScript file (DEPRECARED)

    Note that this file is deprecated.

``dictdumper.html`` contains ``HTML`` only, which dumpers a
JavaScript file according to ``Vue.js`` framework. However,
due to errors in grammar, the output file won't work, thus
it is now deprecated. Usage sample is described as below.

    >>> dumper = JavaScript(file_name)
    >>> dumper(content_dict_1, name=content_name_1)
    >>> dumper(content_dict_2, name=content_name_2)
    ............

"""
import collections
import os
import textwrap


# Writer for JavaScript files
# Dump a JavaScript file for PCAP analyser


from dictdumper.json import JSON


__all__ = ['JavaScript']


# head
_HEADER_START = '''\
// demo data
var data = {
'''


# tail
_HEADER_END = """
}

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


class JavaScript(JSON):
    """Dump JavaScript file under `Vue.js` framework.

    Usage:
        >>> dumper = JavaScript(file_name)
        >>> dumper(content_dict_1, name=content_name_1)
        >>> dumper(content_dict_2, name=content_name_2)
        ............

    Properties:
        * kind - str, return 'js'

    Methods:
        * object_hook - default/customised object hooks

    Attributes:
        * _file - FileIO, output file
        * _sptr - int (file pointer), indicates start of appending point
        * _tctr - int, tab level counter
        * _hrst - str, _HEADER_START
        * _hend - str, _HEADER_END
        * _vctr - dict, value counter dict

    Utilities:
        * _dump_header - initially dump file heads and tails
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
    _vctr = collections.defaultdict(int)    # value counter dict
