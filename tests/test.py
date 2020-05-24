# -*- coding: utf-8 -*-
"""Unittest cases."""

from __future__ import unicode_literals

import collections
import datetime
import os
import tempfile
import unittest
import sys

import dictdumper

PY2 = '.py2' if sys.version_info.major < 3 else ''

try:
    from tempfile import TemporaryDirectory
except ImportError:
    import contextlib
    import shutil

    @contextlib.contextmanager
    def TemporaryDirectory(suffix=None, prefix=None, dir=None):  # pylint: disable=redefined-builtin
        if suffix is None:
            suffix = ''
        if prefix is None:
            prefix = tempfile.template
        if dir is None:
            dir = tempfile.gettempdir()
        tempdir = tempfile.mkdtemp(suffix, prefix, dir)

        try:
            yield tempdir
        except ImportError:
            shutil.rmtree(tempdir)


ROOT = os.path.dirname(os.path.realpath(__file__))

test_1 = collections.OrderedDict()
test_1['foo'] = -1
test_1['bar'] = u'Hello, world!'
test_1['boo'] = collections.OrderedDict()
test_1['boo']['foo_again'] = True
test_1['boo']['bar_again'] = memoryview(b'bytes')
test_1['boo']['boo_again'] = None

test_2 = collections.OrderedDict()
test_2['foo'] = [1, 2.0, 3]
test_2['bar'] = (1.0, bytearray(b'a long long bytes'), 3.0)
test_2['boo'] = collections.OrderedDict()
test_2['boo']['foo_again'] = b'bytestring'
test_2['boo']['bar_again'] = datetime.datetime(2020, 1, 31, 20, 15, 10, 163010)
test_2['boo']['boo_again'] = float('-inf')

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


class TestDictDumper(unittest.TestCase):
    """Test DictDumper."""

    maxDiff = None

    def assertFile(self, first, second):
        with open(first) as file:
            text_first = file.read()
        with open(second) as file:
            text_second = file.read()
        self.assertEqual(text_first, text_second)

    def test_json(self):
        """Test JSON dumper."""
        rootdir = os.path.join(ROOT, 'json')
        with TemporaryDirectory() as tempdir:
            for index in range(2):
                dst = os.path.join(tempdir, 'test_%s.json' % index)

                dumper = dictdumper.JSON(dst)
                self.assertFile(dst, os.path.join(rootdir, 'test_0%s.json' % PY2))

                dumper(test_1, name='test_1')
                self.assertFile(dst, os.path.join(rootdir, 'test_1%s.json' % PY2))

                dumper(test_2, name='test_2')
                self.assertFile(dst, os.path.join(rootdir, 'test_2%s.json' % PY2))

                dumper(test_3, name='test_3')
                self.assertFile(dst, os.path.join(rootdir, 'test_3%s.json' % PY2))

    def test_plist(self):
        """Test PLIST dumper."""
        rootdir = os.path.join(ROOT, 'plist')
        with TemporaryDirectory() as tempdir:
            for index in range(2):
                dst = os.path.join(tempdir, 'test_%s.plist' % index)

                dumper = dictdumper.PLIST(dst)
                self.assertFile(dst, os.path.join(rootdir, 'test_0%s.plist' % PY2))

                dumper(test_1, name='test_1')
                self.assertFile(dst, os.path.join(rootdir, 'test_1%s.plist' % PY2))

                dumper(test_2, name='test_2')
                self.assertFile(dst, os.path.join(rootdir, 'test_2%s.plist' % PY2))

                dumper(test_3, name='test_3')
                self.assertFile(dst, os.path.join(rootdir, 'test_3%s.plist' % PY2))

    def test_tree(self):
        """Test text tree dumper."""
        rootdir = os.path.join(ROOT, 'tree')
        with TemporaryDirectory() as tempdir:
            for index in range(2):
                dst = os.path.join(tempdir, 'test_%s.txt' % index)

                dumper = dictdumper.Tree(dst)
                self.assertFile(dst, os.path.join(rootdir, 'test_0%s.txt' % PY2))

                dumper(test_1, name='test_1')
                self.assertFile(dst, os.path.join(rootdir, 'test_1%s.txt' % PY2))

                dumper(test_2, name='test_2')
                self.assertFile(dst, os.path.join(rootdir, 'test_2%s.txt' % PY2))

                dumper(test_3, name='test_3')
                self.assertFile(dst, os.path.join(rootdir, 'test_3%s.txt' % PY2))


if __name__ == "__main__":
    unittest.main()
