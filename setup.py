#!/usr/bin/python3
# -*- coding: utf-8 -*-


import setuptools


# README
with open('./README.md', 'r') as file:
    long_desc = file.read()


# version string
__version__ = '0.4.1'


# set-up script for pip distribution
setuptools.setup(
    name = 'jsformat',
    version = __version__,
    author = 'Jarry Shaw',
    author_email = 'jarryshaw@icloud.com',
    url = 'https://github.com/JarryShaw/jsformat',
    license = 'GNU General Public License v3 (GPLv3)',
    keywords = 'formatting dumper stream',
    description = 'A stream format output dumper.',
    long_description = long_desc,
    long_description_content_type='text/markdown',
    install_requires = ['setuptools'],
    python_requires = '>=3.0',
    py_modules = ['jsformat'],
    packages = ['jsformat'],
    package_data = {
        '': [
            'LICENSE',
            'README.md',
        ],
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: System :: Networking',
        'Topic :: Utilities',
    ]
)
