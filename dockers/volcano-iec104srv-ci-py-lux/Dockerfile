FROM debian:9.5-slim

RUN apt-get update

# gcc for Twisted
RUN apt-get install --yes python3 python3-pip gcc

RUN apt-get install --yes git

# Cache
RUN pip3 install twisted coverage

