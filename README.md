# aquascope_backend

## Environment files
In order to run the stack you need to setup a few environment files and fill required values.

### celery.env
* RABBITMQ_DEFAULT_PASS - password used for celery/rabbitmq authentication. Should be the same as `CELERY_PASS`
* CELERY_PASS - password used for celery/rabbitmq authentication. Should be the same as `RABBITMQ_DEFAULT_PASS`

## Run the stack locally
In orded to run the stack locally you need to define all required environment files and execute the following commands:
```bash
docker-compose build
docker-compose up -d
```
