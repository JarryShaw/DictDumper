#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

if sys.version_info[0] <= 2:
    raise OSError("DictDumper does not support Python 2!")

try:
    from setuptools import setup
    from setuptools.command.bdist_wheel import bdist_wheel
    from setuptools.command.build_py import build_py
    from setuptools.command.develop import develop
    from setuptools.command.install import install
    from setuptools.command.sdist import sdist
except ImportError:
    raise ImportError("setuptools is required to install DictDumper!")

# get logger
logger = logging.getLogger("pcapkit.setup")
formatter = logging.Formatter(
    fmt="[%(levelname)s] %(asctime)s - %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
)
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_long_description() -> 'str':
    """Extract description from README.md, for PyPI's usage."""
    with open('README.md', encoding='utf-8') as file:
        long_description = file.read()
    return long_description


def refactor(path: 'str') -> 'None':
    """Refactor code."""
    import subprocess  # nosec: B404

    if sys.version_info < (3, 6):
        try:
            subprocess.check_call(  # nosec
                [sys.executable, '-m', 'f2format', '--no-archive', path]
            )
        except subprocess.CalledProcessError as error:
            print('Failed to perform assignment expression backport compiling.'
                  'Please consider manually install `bpc-f2format` and try again.', file=sys.stderr)
            sys.exit(error.returncode)

    if sys.version_info < (3, 8):
        try:
            subprocess.check_call(  # nosec
                [sys.executable, '-m', 'walrus', '--no-archive', path]
            )
        except subprocess.CalledProcessError as error:
            print('Failed to perform assignment expression backport compiling.'
                  'Please consider manually install `bpc-walrus` and try again.', file=sys.stderr)
            sys.exit(error.returncode)

        try:
            subprocess.check_call(  # nosec
                [sys.executable, '-m', 'poseur', '--no-archive', path]
            )
        except subprocess.CalledProcessError as error:
            print('Failed to perform assignment expression backport compiling.'
                  'Please consider manually install `bpc-poseur` and try again.', file=sys.stderr)
            sys.exit(error.returncode)


class dictdumper_sdist(sdist):
    """Modified sdist to run PyBPC conversion."""

    def make_release_tree(self, base_dir: 'str', *args: 'Any', **kwargs: 'Any') -> 'None':
        super(dictdumper_sdist, self).make_release_tree(base_dir, *args, **kwargs)
        logger.info("running sdist")

        # PyBPC compatibility enforcement
        #refactor(os.path.join(base_dir, 'dictdumper'))


class dictdumper_build_py(build_py):
    """Modified build_py to run PyBPC conversion."""

    def build_package_data(self) -> 'None':
        super(dictdumper_build_py, self).build_package_data()
        logger.info("running build_py")

        # PyBPC compatibility enforcement
        # refactor(os.path.join(self.build_lib, 'dictdumper'))


class dictdumper_develop(develop):
    """Modified develop to run PyBPC conversion."""

    def run(self) -> 'None':
        super(dictdumper_develop, self).run()
        logger.info("running develop")

        # PyBPC compatibility enforcement
        # refactor(os.path.join(self.install_lib, 'dictdumper'))


class dictdumper_install(install):
    """Modified install to run PyBPC conversion."""

    def run(self) -> 'None':
        super(dictdumper_install, self).run()
        logger.info("running install")

        # PyBPC compatibility enforcement
        # refactor(os.path.join(self.install_lib, 'dictdumper'))  # type: ignore[arg-type]


class dictdumper_bdist_wheel(bdist_wheel):
    """Modified bdist_wheel to run PyBPC conversion."""

    def run(self) -> "None":
        super(dictdumper_bdist_wheel, self).run()
        logger.info("running bdist_wheel")

        # PyBPC compatibility enforcement
        # refactor(os.path.join(self.dist_dir, "dictdumper"))  # type: ignore[arg-type]


setup(
    cmdclass={
        'sdistdictdumper_': dictdumper_sdist,
        'build_py': dictdumper_build_py,
        'develop': dictdumper_develop,
        'install': dictdumper_install,
        'bdist_wheel': dictdumper_bdist_wheel,
    },
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
)
