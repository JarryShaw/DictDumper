# DictDumper

&emsp; The `dictdumper` project is an open source Python program works as a stream formatted output dumper for `dict`.

- [About](#about)
    * `dictdumper.Dumper`
    * `dictdumper.JSON`
    * `dictdumper.PLIST`
    * `dictdumper.Tree`
    * `dictdumper.XML`
    * `dictdumper.HTML`
- [Installation](#installation)
- [Usage](#usage)

---

### About

&emsp; Currently, it supports following formats --

 - `dictdumper.Dumper` -- abstract base class of all dumpers
 - `dictdumper.JSON` -- dump JavaScript object notation (`JSON`) format file
 - `dictdumper.PLIST` -- dump Apple property list (`PLIST`) format file
 - `dictdumper.Tree` -- dump tree-view text (`TXT`) format file
 - `dictdumper.XML` -- dump extensible markup language (`XML`) file (__base class__)
 - `dictdumper.HTML` -- dump JavaScript file under `Vue.js` framework (__DEPRECATED__)

![](https://github.com/JarryShaw/dictdumper/blob/master/doc/dictdumper.png)

&nbsp;

### Installation:

> Note that `dictdumper` supports Python versions __2.7__ and all versions __since 3.0__

```
pip install dictdumper
```

&nbsp;

### Usage

&emsp; `dictdumper` is quite easy to use. After installation, importation, and initialisation, you can simple call the instance to dump contents.

> Take `dictdumper.Tree` for example

```python
import dictdumper
dumper = dictdumper.Tree('out.txt')
test_1 = dict(
    foo=-1,
    bar='Hello, world!',
    boo=dict(
        foo_again=True,
        bar_again=memoryview(b'bytes'),
        boo_again=None,
    ),
)
dumper(test_1, name='test_1')
```
```
$ cat out.txt
test_1
  |-- foo -> -1
  |-- bar -> Hello, world!
  |-- boo
        |-- foo_again -> True
        |-- bar_again
        |     |-- type -> memoryview
        |     |-- value -> 62 79 74 65 73
        |     |-- text -> bytes
        |-- boo_again -> NIL
```
```python
import datetime
test_2 = dict(
    foo=[1, 2.0, 3],
    bar=(1.0, bytearray(b'a long long bytes'), 3.0),
    boo=dict(
        foo_again=b'bytestring',
        bar_again=datetime.datetime(2020, 1, 31, 20, 15, 10, 163010),
        boo_again=float('-inf'),
    ),
)
dumper(test_2, name='test_2')
```
```
$ cat out.txt
test_1
  |-- foo -> -1
  |-- bar -> Hello, world!
  |-- boo
        |-- foo_again -> True
        |-- bar_again
        |     |-- type -> memoryview
        |     |-- value -> 62 79 74 65 73
        |     |-- text -> bytes
        |-- boo_again -> NIL

test_2
  |-- foo
  |     |--> 1
  |     |--> 2.0
  |     |--> 3
  |-- bar
  |     |-- type -> tuple
  |     |-- value
  |           |--> 1.0
  |           |--> --
  |           |     |-- type -> bytearray
  |           |     |-- value
  |           |     |     |--> 61 20 6c 6f 6e 67 20 6c 6f 6e 67 20 62 79 74 65
  |           |     |          73
  |           |     |-- text -> a long long bytes
  |           |--> 3.0
  |-- boo
        |-- foo_again -> 62 79 74 65 73 74 72 69 6e 67
        |-- bar_again -> 2020-01-31T20:15:10.163010
        |-- boo_again -> -Infinity
```
```python
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
dumper(test_3, name='test_3')
```
```
$ cat out.txt
test_1
  |-- foo -> -1
  |-- bar -> Hello, world!
  |-- boo
        |-- foo_again -> True
        |-- bar_again
        |     |-- type -> memoryview
        |     |-- value -> 62 79 74 65 73
        |     |-- text -> bytes
        |-- boo_again -> NIL

test_2
  |-- foo
  |     |--> 1
  |     |--> 2.0
  |     |--> 3
  |-- bar
  |     |-- type -> tuple
  |     |-- value
  |           |--> 1.0
  |           |--> --
  |           |     |-- type -> bytearray
  |           |     |-- value
  |           |     |     |--> 61 20 6c 6f 6e 67 20 6c 6f 6e 67 20 62 79 74 65
  |           |     |          73
  |           |     |-- text -> a long long bytes
  |           |--> 3.0
  |-- boo
        |-- foo_again -> 62 79 74 65 73 74 72 69 6e 67
        |-- bar_again -> 2020-01-31T20:15:10.163010
        |-- boo_again -> -Infinity

test_3
  |-- foo
  |     |--> stringstringstringstringstringstringstri
  |          ngstringstringstring
  |-- bar
  |     |--> s1
  |     |--> False
  |     |--> s3
  |-- boo
  |     |--> s4
  |     |--> --
  |     |     |-- s -> 5
  |     |     |-- j -> 5
  |     |--> s6
  |-- far
  |     |-- far_foo
  |     |     |--> s1
  |     |     |--> s2
  |     |     |--> s3
  |     |-- far_var -> s4
  |-- biu -> NaN
```
