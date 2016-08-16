FROM ubuntu:xenial
MAINTAINER Domestique Studios <support@domestiquestudios.com>

ENV LANG=C.UTF-8
RUN dpkg-divert --local --rename --add /sbin/initctl && \
    apt-get update && \
    apt-get -y install build-essential python3 python3-dev python3-setuptools git \
        ca-certificates libpq-dev nginx cron libffi-dev vim libncurses5-dev libncurses5 \
        docker.io && \
    /usr/bin/easy_install3 -UaZ pip && \
    mkdir -p /home/docker/pannier/ /var/log/uwsgi /usr/local/pannier/static /usr/local/pannier/media

ADD . /home/docker/pannier/
WORKDIR /home/docker/pannier/pannier/
RUN /usr/local/bin/pip3.5 install -r ../requirements.txt  -r ../testing_requirements.txt && \
    python3 setup.py develop
WORKDIR /home/docker/pannier/pannier_project
RUN unlink /etc/nginx/sites-enabled/default && \
    ln -s /home/docker/pannier/configs/nginx/pannier.conf /etc/nginx/sites-enabled

cmd ["./startup.sh"]
