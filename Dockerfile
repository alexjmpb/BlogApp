# pull official base image
FROM python:3.9-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN apk add zlib-dev jpeg-dev gcc musl-dev
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# copy project
COPY . .

RUN python manage.py collectstatic --noinput

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# run gunicorn
CMD gunicorn settings.wsgi:application --bind 0.0.0.0:$PORT