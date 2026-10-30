# -*- coding: utf-8 -*-
"""Unittest cases."""

from __future__ import unicode_literals

import collections
import datetime
import json
import os
import tempfile
import unittest
import sys

import dictdumper

PY2 = '.py2' if sys.version_info.major < 3 else ''

try:
    from plistlib import load as load_plist
except ImportError:
    from plistlib import readPlist as load_plist

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

# Keys and values holding characters that are special to the output formats,
# c.f. https://github.com/JarryShaw/DictDumper/issues/121. Every key here is
# also used as a value, so that a dumper escaping only one of the two is caught.
test_escape = collections.OrderedDict()
test_escape[u'quote"key'] = u'quote"value'
test_escape[u'back\\slash'] = u'back\\slash'
test_escape[u'amp&key'] = u'lt<gt>value'
test_escape[u'nested'] = collections.OrderedDict()
test_escape[u'nested'][u'tab\tkey'] = u'tab\tvalue'

# A non-string key, which is rendered through ``str()``. On Python 3 that is a
# ``bytes`` repr and carries quotation marks; on Python 2 it is the bytes
# themselves. Either way the rendering holds a character needing escaping.
test_bytes_key = collections.OrderedDict()
test_bytes_key[b'\x20\x21\x22\x23'] = u'client random'

# A ``datetime`` carrying microseconds, which a property list ``<date>`` has no
# field for, and a bare ``date``, which carries no time of day at all. C.f.
# https://github.com/JarryShaw/DictDumper/issues/122.
test_date = collections.OrderedDict()
test_date['stamp'] = datetime.datetime(2020, 1, 31, 20, 15, 10, 163010)
test_date['day'] = datetime.date(2020, 1, 31)


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

    def test_json_escape(self):
        """Test JSON dumper escapes mapping keys."""
        with TemporaryDirectory() as tempdir:
            dst = os.path.join(tempdir, 'test_escape.json')

            dumper = dictdumper.JSON(dst)
            dumper(test_escape, name='esc"ape')
            dumper(test_bytes_key, name='bytes')

            with open(dst) as file:
                report = json.load(file)

            self.assertEqual(sorted(report), ['bytes', 'esc"ape'])
            self.assertEqual(report['esc"ape'], {
                'quote"key': 'quote"value',
                'back\\slash': 'back\\slash',
                'amp&key': 'lt<gt>value',
                'nested': {'tab\tkey': 'tab\tvalue'},
            })
            self.assertEqual(list(report['bytes'].values()), ['client random'])

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

    def test_plist_escape(self):
        """Test PLIST dumper escapes mapping keys and string values."""
        with TemporaryDirectory() as tempdir:
            dst = os.path.join(tempdir, 'test_escape.plist')

            dumper = dictdumper.PLIST(dst)
            dumper(test_escape, name='esc&ape')
            dumper(test_bytes_key, name='bytes')

            with open(dst, 'rb') as file:
                report = load_plist(file)

            self.assertEqual(sorted(report), ['bytes', 'esc&ape'])
            self.assertEqual(report['esc&ape'], {
                'quote"key': 'quote"value',
                'back\\slash': 'back\\slash',
                'amp&key': 'lt<gt>value',
                'nested': {'tab\tkey': 'tab\tvalue'},
            })
            self.assertEqual(list(report['bytes'].values()), ['client random'])

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

    def test_plist_date(self):
        """Test PLIST dumper writes a date plistlib can read."""
        with TemporaryDirectory() as tempdir:
            dst = os.path.join(tempdir, 'test_date.plist')

            dumper = dictdumper.PLIST(dst)
            dumper(test_date, name='test_date')

            with open(dst, 'rb') as file:
                report = load_plist(file)

            # the microseconds are gone -- a <date> has no field for them
            self.assertEqual(report['test_date'], {
                'stamp': datetime.datetime(2020, 1, 31, 20, 15, 10),
                'day': datetime.datetime(2020, 1, 31, 0, 0),
            })


if __name__ == "__main__":
    unittest.main()
