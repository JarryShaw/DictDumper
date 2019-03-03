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
    foo = -1,                   # int
    bar = 'Hello, world!',      # string
    boo = dict(                 # dict
        foo_again = True,       # bool
        bar_again = b'bytes',   # bytes (b'\x62\x79\x74\x65\x73')
        boo_again = None,       # NoneType
    ),
)
dumper(test_1, name='test_1')
```
```
$ cat out.txt
PCAP File Tree-View Format

test
  |-- foo -> -1
  |-- bar -> hello
  |-- boo
        |-- foo_again -> True
        |-- bar_again -> 62 79 74 65 73
        |-- boo_again -> N/A
```
```python
import datetime
test_2 = dict(
    foo = [1, 2.0, 3],          # list
    bar = (1.0, 2, 3.0),        # tuple
    boo = dict(                 # dict
        foo_again = 'a long long bytes',
                                # bytes
        bar_again = datetime.datetime.today(),
                                # datetime
        boo_again = -1.0,       # float
    ),
)
dumper(test_2, name='test_2')
```
```
$ cat out.txt
PCAP File Tree-View Format

test_1
  |-- foo -> -1
  |-- bar -> Hello, world!
  |-- boo
        |-- foo_again -> True
        |-- bar_again -> 62 79 74 65 73
        |-- boo_again -> N/A

test_2
  |-- foo
  |     |--> 1
  |     |--> 2.0
  |     |--> 3
  |-- bar
  |     |--> 1.0
  |     |--> 2
  |     |--> 3.0
  |-- boo
        |-- foo_again -> a long long bytes
        |-- bar_again -> 2018-03-08 17:47:35
        |-- boo_again -> -1.0
```
