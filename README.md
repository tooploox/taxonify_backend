# aquascope_backend

## Environment files
In order to run the stack you need to setup a few environment files and fill required values.

### celery.env
* RABBITMQ_DEFAULT_PASS - password used for celery/rabbitmq authentication. Should be the same as `CELERY_PASS`
* CELERY_PASS - password used for celery/rabbitmq authentication. Should be the same as `RABBITMQ_DEFAULT_PASS`

### mongodb.env
* MONGO_INITDB_ROOT_USERNAME - db username
* MONGO_INITDB_ROOT_PASSWORD - db password
* MONGO_INITDB_DATABASE - db name

### mongodb_credentials.env
* MONGO_CONNECTION_STRING - should be consistent with the content of `mongodb.env` file. It should be `mongodb://<MONGO_INITDB_ROOT_USERNAME>:<MONGO_INITDB_ROOT_PASSWORD>@<DB_ADDRESS>/<MONGO_INITDB_DATABASE>`. `<DB_ADDRESS>` for local stack is just `mongo`.

### user_authentication.env
* JWT_SECRET_KEY - key for signing JWT tokens
* AQUASCOPE_TEST_USER - username of the only user in the system
* AQUASCOPE_TEST_PASS - password of the only user in the system encoded with `pbkdf2_sha256` algorithm from `passlib` library.


## Run the stack locally
In orded to run the stack locally you need to define all required environment files and execute the following commands:
```bash
docker-compose build
docker-compose up -d
```
