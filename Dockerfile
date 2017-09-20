FROM phusion/baseimage:latest
MAINTAINER Yibai Zhang <xm1994@outlook.com> From Asuri Team

ENV HOME /root

# Replace mirrors to tsinghua and install some dependence
RUN sed -i s/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list \
    && sed -i s/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y build-essential sudo gcc-multilib libtool libtool-bin unzip nasm clang python python-pip python-wheel git automake autoconf bison debootstrap debian-archive-keyring \
    && apt-get build-dep -y qemu \
    && apt-get clean \
    && mkdir $HOME/.pip && printf "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" > $HOME/.pip/pip.conf \
    && pip install --upgrade pip \
    && pip install virtualenv \
    && mkdir -p /opt/asuri-robot && virtualenv /opt/asuri-robot \
    && rm -rf /tmp/* /var/tmp/* && rm -rf /var/lib/apt/lists/* && rm -f /etc/ssh/ssh_host_*



# Install robot related python packages
RUN bash -c "source /opt/asuri-robot/bin/activate \
    && pip install --no-binary :all: capstone \
    && mkdir -p /opt/asuri-robot/tmp/ \
    && cd /opt/asuri-robot/tmp/ \
    && wget https://github.com/angr/angr/archive/master.zip \
    && unzip master.zip && rm master.zip && mv angr-master angr \
    && cd angr && pip install --no-binary :all: . \
    && cd /opt/asuri-robot/tmp/ \
    && wget https://github.com/shellphish/shellphish-afl/archive/master.zip \
    && unzip master.zip && rm master.zip && mv shellphish-afl-master shellphish-afl \
    && cd shellphish-afl && pip install --no-binary :all: . \
    && cd /opt/asuri-robot/tmp/ \
    && wget https://github.com/shellphish/shellphish-qemu/archive/master.zip \
    && unzip master.zip && rm master.zip && mv shellphish-qemu-master shellphish-qemu \
    && cd shellphish-qemu && pip install --no-binary :all: . \
    && cd /opt/asuri-robot/tmp/ \
    && wget https://github.com/shellphish/driller/archive/master.zip \
    && unzip master.zip && rm master.zip && mv driller-master driller \
    && cd driller && pip install --no-binary :all: . \
    && cd /opt/asuri-robot/tmp/ \
    && wget https://github.com/shellphish/fuzzer/archive/master.zip \
    && unzip master.zip && rm master.zip && mv fuzzer-master fuzzer \
    && cd fuzzer && pip install --no-binary :all: . \
    && mkdir -p /opt/asuri-robot/tmp/ \
    && cd /opt/asuri-robot/tmp/ \
    && wget https://github.com/mechaphish/povsim/archive/master.zip \
    && unzip master.zip && rm master.zip && mv povsim-master povsim \
    && cd povsim && pip install --no-binary :all: . \
    && cd /opt/asuri-robot/tmp/ \
    && wget https://github.com/mechaphish/compilerex/archive/master.zip \
    && unzip master.zip && rm master.zip && mv compilerex-master compilerex \
    && cd compilerex && pip install --no-binary :all: . \
    && cd /opt/asuri-robot/tmp/ \
    && wget https://github.com/angr/fidget/archive/master.zip \
    && unzip master.zip && rm master.zip && mv fidget-master fidget \
    && cd fidget && pip install --no-binary :all: . \
    && cd /opt/asuri-robot/tmp/ \
    && wget https://github.com/shellphish/rex/archive/master.zip \
    && unzip master.zip && rm master.zip && mv rex-master rex \
    && cd rex && pip install --no-binary :all: . \
    && cd /opt/asuri-robot/tmp/ \
    && wget https://github.com/shellphish/patcherex/archive/master.zip \
    && unzip master.zip && rm master.zip && mv patcherex-master patcherex && cd patcherex \
    && pip install --no-binary :all: . \
    && rm -fr /opt/asuri-robot/tmp" \
    && rm -rf /tmp/* /var/tmp/* && rm -rf /var/lib/apt/lists/* && rm -f /etc/ssh/ssh_host_*

