FROM python:3.6

RUN pip3 install git+https://github.com/pypa/pipenv.git@419e0310e458d0eca5ad0585c9204e6557650335
ADD Pipfile* /app/
WORKDIR /app

RUN pipenv install --dev --system --deploy

ADD . /app

ENV ENVIRONMENT "dev"

ENTRYPOINT gunicorn --bind ':8000' --reload aquascope.webserver.app:app
