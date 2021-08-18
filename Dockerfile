FROM python:3.8-slim-buster

RUN pip install cloverwallpaper==0.6.7 && \
    mkdir /home/cloverwallpaper

WORKDIR /home/cloverwallpaper
ENTRYPOINT [ "cloverwallpaper" ]