FROM python:3.8-slim

LABEL maintainer "Kyrylo Malakhov <malakhovks@nas.gov.ua>"
LABEL description "Stanza library inside docker container demo."

COPY . /stanza/serv
WORKDIR /stanza/serv

RUN apt-get -y clean \
    && apt-get -y update \
    && apt-get -y install nginx \
    && apt-get -y install python-dev \
    && apt-get -y install build-essential \
    && apt-get -y install curl \
    && curl https://getmic.ro | bash \
    # ------------------------------------------------------------------
    && pip install -r ./deploy/requirements.txt --src /usr/local/src \
    && rm -r /root/.cache \
    && apt-get -y clean \
    && apt-get -y autoremove

COPY ./deploy/nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]
