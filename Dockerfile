FROM ubuntu:latest
MAINTAINER Dev Jha <i.dnjha@gmail.com>
RUN apt-get update && apt-get install -y wget gcc
RUN wget https://raw.githubusercontent.com/jeffhammond/STREAM/master/stream.c
RUN gcc -O stream.c -o stream
CMD ./stream
