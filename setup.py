#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from distutils.cmd import Command
    from typing import Any, Type

if sys.version_info[0] <= 2:
    raise OSError("DictDumper does not support Python 2!")

try:
    from setuptools import setup
except ImportError:
    raise ImportError("setuptools is required to install DictDumper!")

# get logger
logger = logging.getLogger("dictdumper.setup")
formatter = logging.Formatter(
    fmt="[%(levelname)s] %(asctime)s - %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
)
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_long_description() -> "str":
    """Extract description from README.md, for PyPI's usage."""
    with open("README.md", encoding="utf-8") as file:
        long_description = file.read()
    return long_description


def refactor(path: "str") -> "None":
    """Refactor code."""
    import subprocess  # nosec: B404

    if sys.version_info < (3, 6):
        try:
            subprocess.check_call(  # nosec
                [sys.executable, "-m", "f2format", "--no-archive", path]
            )
        except subprocess.CalledProcessError as error:
            logger.error(
                "Failed to perform assignment expression backport compiling. "
                "Please consider manually install `bpc-f2format` and try again."
            )
            sys.exit(error.returncode)

    if sys.version_info < (3, 8):
        try:
            subprocess.check_call(  # nosec
                [sys.executable, "-m", "walrus", "--no-archive", path]
            )
        except subprocess.CalledProcessError as error:
            logger.error(
                "Failed to perform assignment expression backport compiling. "
                "Please consider manually install `bpc-walrus` and try again."
            )
            sys.exit(error.returncode)

        try:
            subprocess.check_call(  # nosec
                [sys.executable, "-m", "poseur", "--no-archive", path]
            )
        except subprocess.CalledProcessError as error:
            logger.error(
                "Failed to perform assignment expression backport compiling. "
                "Please consider manually install `bpc-poseur` and try again."
            )
            sys.exit(error.returncode)


cmdclass = {}  # type: dict[str, Type[Command]]

try:
    from setuptools.command.sdist import sdist

    class dictdumper_sdist(sdist):
        """Modified sdist to run PyBPC conversion."""

        def make_release_tree(
            self, base_dir: "str", *args: "Any", **kwargs: "Any"
        ) -> "None":
            super(dictdumper_sdist, self).make_release_tree(base_dir, *args, **kwargs)
            logger.info("running sdist")

            # PyBPC compatibility enforcement
            #refactor(os.path.join(base_dir, "dictdumper"))

    cmdclass["sdist"] = dictdumper_sdist
except ImportError:
    logger.warning(
        "setuptools version is too old to support PyBPC conversion in sdist."
    )

try:
    from setuptools.command.build_py import build_py

    class dictdumper_build_py(build_py):
        """Modified build_py to run PyBPC conversion."""

        def build_package_data(self) -> "None":
            super(dictdumper_build_py, self).build_package_data()
            logger.info("running build_py")

            # PyBPC compatibility enforcement
            #refactor(os.path.join(self.build_lib, "dictdumper"))

    cmdclass["build_py"] = dictdumper_build_py
except ImportError:
    logger.warning(
        "setuptools version is too old to support PyBPC conversion in build_py."
    )

try:
    from setuptools.command.develop import develop

    class dictdumper_develop(develop):
        """Modified develop to run PyBPC conversion."""

        def run(self) -> "None":  # type: ignore[override]
            super(dictdumper_develop, self).run()
            logger.info("running develop")

            # PyBPC compatibility enforcement
            #refactor(os.path.join(self.install_lib, "dictdumper"))

    cmdclass["develop"] = dictdumper_develop
except ImportError:
    logger.warning(
        "setuptools version is too old to support PyBPC conversion in develop."
    )

try:
    from setuptools.command.install import install

    class dictdumper_install(install):
        """Modified install to run PyBPC conversion."""

        def run(self) -> "None":
            super(dictdumper_install, self).run()
            logger.info("running install")

            # PyBPC compatibility enforcement
            #refactor(os.path.join(self.install_lib, "dictdumper"))  # type: ignore[arg-type]

    cmdclass["install"] = dictdumper_install
except ImportError:
    logger.warning(
        "setuptools version is too old to support PyBPC conversion in install."
    )

try:
    from setuptools.command.bdist_wheel import bdist_wheel

    class dictdumper_bdist_wheel(bdist_wheel):
        """Modified bdist_wheel to run PyBPC conversion."""

        def run(self) -> "None":
            super(dictdumper_bdist_wheel, self).run()
            logger.info("running bdist_wheel")

            # PyBPC compatibility enforcement
            #refactor(os.path.join(self.dist_dir, "dictdumper"))  # type: ignore[arg-type]

    cmdclass["bdist_wheel"] = dictdumper_bdist_wheel
except ImportError:
    logger.warning(
        "setuptools version is too old to support PyBPC conversion in bdist_wheel."
    )

setup(
    cmdclass=cmdclass,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
)
