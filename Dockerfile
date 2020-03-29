FROM python:3.7
MAINTAINER Stephen Greene (sxg6123@rit.edu)
MAINTAINER Joel Eeager (jee7291@rit.edu)

WORKDIR /app

RUN apt-get update
RUN apt-get install -y openssl python-dev libsasl2-dev libldap2-dev python-mysqldb

COPY . /app
RUN pip install pyopenssl
RUN pip install -r requirements.txt

ENTRYPOINT /bin/bash
