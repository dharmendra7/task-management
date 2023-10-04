FROM python:3.8
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
#COPY ./requirements/base.txt ./requirements/local.txt ./

COPY . /code
WORKDIR /code


RUN apt-get update -y
RUN apt-get install redis redis-server -y
RUN service redis-server start
#RUN django-admin compilemessages -l ar
RUN pip install -r ./requirements.txt

# Adds our application code to the image
EXPOSE 8000
