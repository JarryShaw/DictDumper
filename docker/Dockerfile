# basic info
FROM library/ubuntu
LABEL version 2019.02.26
LABEL description "Ubuntu Environment"

# prepare environment
ENV LANG "C.UTF-8"
ENV LC_ALL "C.UTF-8"
ENV PYTHONIOENCODING "UTF-8"

# install packages
RUN apt-get update && \
    apt-get install --yes \
        curl \
        software-properties-common && \
    add-apt-repository --yes ppa:pypy/ppa && \
    add-apt-repository --yes ppa:deadsnakes/ppa
RUN apt-get update && \
    apt-get upgrade --yes && \
    apt-get install --yes \
        pypy \
        pypy3 \
        python2.7 \
        python3.4 \
        python3.5 \
        python3.6 \
        python3.7 && \
    apt-get install -y \
        pypy-dev \
        pypy3-dev \
        python-pip \
        python3-pip

# run get-pip.py
RUN mv /usr/local/lib/pypy3 /usr/local/lib/pypy3.5
RUN curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py && \
    python3.7 /tmp/get-pip.py && \
    python3.6 /tmp/get-pip.py && \
    python3.5 /tmp/get-pip.py && \
    python3.4 /tmp/get-pip.py && \
    python2.7 /tmp/get-pip.py && \
    pypy3     /tmp/get-pip.py && \
    pypy      /tmp/get-pip.py

# cleanup process
RUN rm -rf \
        /var/lib/apt/lists/* \
        /tmp/get-pip.py \
        /tmp/pip && \
    apt-get remove --yes \
        curl && \
    apt-get autoremove --yes && \
    apt-get autoclean && \
    apt-get clean

# copy source
COPY . /dictdumper
