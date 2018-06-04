FROM ziedguesmi/opencv:3-raspbian

LABEL maintainer="Zied Guesmi <guesmy.zied@gmail.com>"
LABEL version="1.0"

RUN [ "cross-build-start" ]

RUN apt-get update && apt-get install -y --no-install-recommends \
        # libgtk2.0-dev \
        # libpng12-dev \
        python3-pip \
        && \
    pip3 install PyYAML yamlordereddictloader color_transfer && \
    apt-get remove -y python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /iexec

RUN [ "cross-build-end" ]

COPY ./app /color-transfer

WORKDIR /color-transfer

ENTRYPOINT [ "/color-transfer/entrypoint" ]