# -*- coding: utf-8 -*-
"""Unittest cases."""

import datetime
import os
import tempfile
import unittest

import dictdumper

ROOT = os.path.dirname(os.path.realpath(__file__))

test_1 = dict(
    foo=-1,
    bar='Hello, world!',
    boo=dict(
        foo_again=True,
        bar_again=memoryview(b'bytes'),
        boo_again=None,
    ),
)

test_2 = dict(
    foo=[1, 2.0, 3],
    bar=(1.0, bytearray(b'a long long bytes'), 3.0),
    boo=dict(
        foo_again=b'bytestring',
        bar_again=datetime.datetime(2020, 1, 31, 20, 15, 10, 163010),
        boo_again=float('-inf'),
    ),
)

test_3 = dict(
    foo="stringstringstringstringstringstringstringstringstringstring",
    bar=[
        "s1", False, "s3",
    ],
    boo=[
        "s4", dict(s="5", j="5"), "s6"
    ],
    far=dict(
        far_foo=["s1", "s2", "s3"],
        far_var="s4",
    ),
    biu=float('nan'),
)


class TestDictDumper(unittest.TestCase):
    """Test DictDumper."""

    def assertFile(self, first, second):
        with open(first) as file:
            text_first = file.read()
        with open(second) as file:
            text_second = file.read()
        self.assertEqual(text_first, text_second)

    def test_json(self):
        """Test JSON dumper."""
        rootdir = os.path.join(ROOT, 'json')
        with tempfile.TemporaryDirectory() as tempdir:
            dst = os.path.join(tempdir, 'test.json')

            dumper = dictdumper.JSON(dst)
            self.assertFile(dst, os.path.join(rootdir, 'test_0.json'))

            dumper(test_1, name='test_1')
            self.assertFile(dst, os.path.join(rootdir, 'test_1.json'))

            dumper(test_2, name='test_2')
            self.assertFile(dst, os.path.join(rootdir, 'test_2.json'))

            dumper(test_3, name='test_3')
            self.assertFile(dst, os.path.join(rootdir, 'test_3.json'))

    def test_plist(self):
        """Test PLIST dumper."""
        rootdir = os.path.join(ROOT, 'plist')
        with tempfile.TemporaryDirectory() as tempdir:
            dst = os.path.join(tempdir, 'test.plist')

            dumper = dictdumper.PLIST(dst)
            self.assertFile(dst, os.path.join(rootdir, 'test_0.plist'))

            dumper(test_1, name='test_1')
            self.assertFile(dst, os.path.join(rootdir, 'test_1.plist'))

            dumper(test_2, name='test_2')
            self.assertFile(dst, os.path.join(rootdir, 'test_2.plist'))

            dumper(test_3, name='test_3')
            self.assertFile(dst, os.path.join(rootdir, 'test_3.plist'))

    def test_tree(self):
        """Test text tree dumper."""
        rootdir = os.path.join(ROOT, 'tree')
        with tempfile.TemporaryDirectory() as tempdir:
            dst = os.path.join(tempdir, 'test.txt')

            dumper = dictdumper.Tree(dst)
            self.assertFile(dst, os.path.join(rootdir, 'test_0.txt'))

            dumper(test_1, name='test_1')
            self.assertFile(dst, os.path.join(rootdir, 'test_1.txt'))

            dumper(test_2, name='test_2')
            self.assertFile(dst, os.path.join(rootdir, 'test_2.txt'))

            dumper(test_3, name='test_3')
            self.assertFile(dst, os.path.join(rootdir, 'test_3.txt'))


if __name__ == "__main__":
    unittest.main()
