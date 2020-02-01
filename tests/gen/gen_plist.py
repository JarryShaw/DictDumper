# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import collections
import datetime
import os

import dictdumper

ROOT = os.path.dirname(os.path.realpath(__file__))
dumper_0 = dictdumper.PLIST(os.path.join(ROOT, '..', 'plist', 'test_0.py2.plist'))

test_1 = collections.OrderedDict()
test_1['foo'] = -1
test_1['bar'] = u'Hello, world!'
test_1['boo'] = collections.OrderedDict()
test_1['boo']['foo_again'] = True
test_1['boo']['bar_again'] = memoryview(b'bytes')
test_1['boo']['boo_again'] = None
dumper_1 = dictdumper.PLIST(os.path.join(ROOT, 'plist', 'test_1.py2.plist'))
dumper_1(test_1, 'test_1')

test_2 = collections.OrderedDict()
test_2['foo'] = [1, 2.0, 3]
test_2['bar'] = (1.0, bytearray(b'a long long bytes'), 3.0)
test_2['boo'] = collections.OrderedDict()
test_2['boo']['foo_again'] = b'bytestring'
test_2['boo']['bar_again'] = datetime.datetime(2020, 1, 31, 20, 15, 10, 163010)
test_2['boo']['boo_again'] = float('-inf')
dumper_2 = dictdumper.PLIST(os.path.join(ROOT, 'plist', 'test_2.py2.plist'))
dumper_2(test_1, 'test_1')
dumper_2(test_2, 'test_2')

test_3 = collections.OrderedDict()
test_3['foo'] = u"stringstringstringstringstringstringstringstringstringstring"
test_3['bar'] = [
    u"s1", False, u"s3",
]
test_3['boo'] = [
    u"s4", collections.OrderedDict(), u"s6"
]
test_3['boo'][1]['s'] = u"5"
test_3['boo'][1]['j'] = u"5"
test_3['far'] = collections.OrderedDict()
test_3['far']['far_foo'] = [u"s1", u"s2", u"s3"]
test_3['far']['far_var'] = u"s4"
test_3['biu'] = float('nan')
dumper_3 = dictdumper.PLIST(os.path.join(ROOT, 'plist', 'test_3.py2.plist'))
dumper_3(test_1, 'test_1')
dumper_3(test_2, 'test_2')
dumper_3(test_3, 'test_3')
