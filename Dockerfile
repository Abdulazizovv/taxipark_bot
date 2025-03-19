FROM python:3.12.3-alpine


# RUN apk update \
#     && apk add --no-cache \
#     build-base \
#     mariadb-dev \
#     libffi-dev \
#     python3-dev \
#     && pip install --upgrade pip \
#     && rm -rf /var/cache/apk/*

WORKDIR /usr/src/app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r\
    /usr/src/app/requirements.txt
    
COPY . /usr/src/app/

RUN python manage.py migrate

