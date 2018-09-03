FROM python:3.7

LABEL author="Vladimir Aleshin"
LABEL description="Dockerfile for image check app"

RUN pip3 install pipenv

WORKDIR /usr/src

COPY Pipfile ./
COPY Pipfile.lock ./

RUN set -ex && pipenv install --system --deploy

COPY src/ .
CMD python3 main.py
