FROM python:3.6

RUN pip3 install git+https://github.com/pypa/pipenv.git@419e0310e458d0eca5ad0585c9204e6557650335
ADD Pipfile* /app/
WORKDIR /app

RUN pipenv install --system --deploy

ADD . /app

ENTRYPOINT celery -A aquascope.tasks.celery_app worker --loglevel=info
