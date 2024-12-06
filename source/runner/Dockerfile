ARG TS_WEB_VERSION=latest
FROM ghcr.io/denvilk-bsuir/swdt:ts_web-${TS_WEB_VERSION}

USER root

RUN apk add build-base
RUN apk add cmake git

WORKDIR /testlib
RUN wget https://raw.githubusercontent.com/MikeMirzayanov/testlib/refs/heads/master/testlib.h

WORKDIR /runexe
RUN git clone https://github.com/prodigy-by/runexe .
RUN mkdir build
WORKDIR /runexe/build
RUN cmake ..
RUN make

WORKDIR /app

CMD ["python3", "manage.py", "runner"]