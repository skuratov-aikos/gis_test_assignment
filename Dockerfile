FROM python:3.6

#to show logs
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get upgrade -y

#required for geodjango/postgis
RUN apt-get install -y gdal-bin libgdal-dev
RUN apt-get install -y python3-gdal
RUN apt-get install -y binutils libproj-dev

WORKDIR /var/html/gistest
COPY requirements.txt /var/html/gistest/
RUN pip3 install -r requirements.txt
COPY . /var/html/gistest/
RUN python manage.py makemigrations