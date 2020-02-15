#!/usr/bin/env bash

# print a trace of simple commands
set -ex

# run tests
pipenv run tox || true

# prepare for PyPI distribution
rm -rf build
mkdir -p eggs \
         sdist \
         wheels
[ -d dist ] && mv -f dist/*.egg eggs/ || true
[ -d dist ] && mv -f dist/*.whl wheels/ || true
[ -d dist ] && mv -f dist/*.tar.gz sdist/ || true
rm -rf dist

# make distribution
pipenv run python setup.py sdist bdist_wheel

# distribute to PyPI and TestPyPI
twine check dist/*
twine upload dist/* -r pypi --skip-existing
twine upload dist/* -r pypitest --skip-existing

# get version string
version=$( cat setup.py | grep "^__version__" | sed "s/__version__ = '\(.*\)'/\1/" )

# upload to GitHub
git pull
git add .
if [[ -z "$1" ]] ; then
    git commit -a -S
else
    git commit -a -S -m "$1"
fi
git push

description=$( git log -1 --pretty=%B )
git tag -sm"${description}" "v${version}"
git push --tags

# file new release
go run github.com/aktau/github-release release \
    --user JarryShaw \
    --repo DictDumper \
    --tag "v${version}" \
    --name "DictDumper v${version}" \
    --description "${description}"

# update maintenance information
maintainer changelog
maintainer contributor
maintainer contributing

# aftermath
git pull
git add .
git commit -a -S -m "Regular update after distribution"
git push
