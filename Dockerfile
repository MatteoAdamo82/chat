FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./app/requirements.txt ./

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip uninstall django
RUN pip install -r requirements.txt