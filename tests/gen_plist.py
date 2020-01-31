# -*- coding: utf-8 -*-

import datetime
import os

import dictdumper

ROOT = os.path.dirname(os.path.realpath(__file__))
dumper_0 = dictdumper.PLIST(os.path.join(ROOT, 'plist', 'test_0.plist'))

test_1 = dict(
    foo=-1,
    bar='Hello, world!',
    boo=dict(
        foo_again=True,
        bar_again=memoryview(b'bytes'),
        boo_again=None,
    ),
)
dumper_1 = dictdumper.PLIST(os.path.join(ROOT, 'plist', 'test_1.plist'))
dumper_1(test_1, 'test_1')

test_2 = dict(
    foo=[1, 2.0, 3],
    bar=(1.0, bytearray(b'a long long bytes'), 3.0),
    boo=dict(
        foo_again=b'bytestring',
        bar_again=datetime.datetime(2020, 1, 31, 20, 15, 10, 163010),
        boo_again=float('-inf'),
    ),
)
dumper_2 = dictdumper.PLIST(os.path.join(ROOT, 'plist', 'test_2.plist'))
dumper_2(test_1, 'test_1')
dumper_2(test_2, 'test_2')

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
dumper_3 = dictdumper.PLIST(os.path.join(ROOT, 'plist', 'test_3.plist'))
dumper_3(test_1, 'test_1')
dumper_3(test_2, 'test_2')
dumper_3(test_3, 'test_3')
