FROM ubuntu:16.04

LABEL maintainer="Zied Guesmi <guesmy.zied@gmail.com>"
LABEL version="1.0"

COPY requirements.txt /color-transfer/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
        libgtk2.0-dev \
        python3 \
        python3-pip \
        python3-setuptools \
        && \
    pip3 install -r /color-transfer/requirements.txt --no-cache-dir && \
    rm /color-transfer/requirements.txt && \
    apt-get remove -y python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /iexec

COPY ./app /color-transfer

WORKDIR /color-transfer

ENTRYPOINT [ "/color-transfer/entrypoint" ]