#!/usr/bin/env bash

# print a trace of simple commands
set -ex

# prepare for PyPI distribution
rm -rf build
mkdir -p eggs \
         sdist \
         wheels
mv -f dist/*.egg eggs/
mv -f dist/*.whl wheels/
mv -f dist/*.tar.gz sdist/
rm -rf dist

# fetch platform spec
platform=$( python3 -c "import distutils.util; print(distutils.util.get_platform().replace('-', '_').replace('.', '_'))" )

# make macOS distribution
python3.7 setup.py sdist bdist_egg bdist_wheel --plat-name="${platform}" --python-tag='cp37'
python3.6 setup.py bdist_egg bdist_wheel --plat-name="${platform}" --python-tag='cp36'
python3.5 setup.py bdist_egg bdist_wheel --plat-name="${platform}" --python-tag='cp35'
python3.4 setup.py bdist_egg bdist_wheel --plat-name="${platform}" --python-tag='cp34'
python2.7 setup.py bdist_egg bdist_wheel --plat-name="${platform}" --python-tag='cp27'
pypy3 setup.py bdist_wheel --plat-name="${platform}" --python-tag='pp35'
pypy setup.py bdist_wheel --plat-name="${platform}" --python-tag='pp27'

# make Linux distribution
cd docker
sed "s/LABEL version.*/LABEL version $( date +%Y.%m.%d )/" Dockerfile > Dockerfile.tmp
mv Dockerfile.tmp Dockerfile
docker-compose up --build
cd ..

# distribute to PyPI and TestPyPI
twine check dist/* || :
twine upload dist/* -r pypi --skip-existing
twine upload dist/* -r pypitest --skip-existing

# get version string
version=$( cat setup.py | grep "^__version__" | sed "s/__version__ = '\(.*\)'/\1/" )

# upload to GitHub
git pull
git tag "v${version}"
git add .
if [[ -z "$1" ]] ; then
    git commit -a -S
else
    git commit -a -S -m "$1"
fi
git push

# file new release
go run github.com/aktau/github-release release \
    --user JarryShaw \
    --repo DictDumper \
    --tag "v${version}" \
    --name "DictDumper v${version}" \
    --description "$1"

# update maintenance information
maintainer changelog
maintainer contributor
maintainer contributing

# aftermath
git pull
git add .
git commit -a -S -m "Regular update after distribution"
git push
