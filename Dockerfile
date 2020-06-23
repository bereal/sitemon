FROM python:3.8

RUN mkdir -p /opt/sitemon/
COPY ./sitemon /opt/sitemon/sitemon
COPY setup.py /opt/sitemon
WORKDIR /opt/sitemon

RUN python setup.py install
