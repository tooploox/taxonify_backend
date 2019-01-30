# aquascope_backend

## Environment files
In order to run the stack you need to setup a few environment files and fill required values.

### celery.env
* RABBITMQ_DEFAULT_PASS - password used for celery/rabbitmq authentication. Should be the same as `CELERY_PASS`
* CELERY_PASS - password used for celery/rabbitmq authentication. Should be the same as `RABBITMQ_DEFAULT_PASS`

### mongodb_root_credentials.env
* MONGO_INITDB_ROOT_USERNAME - root db username
* MONGO_INITDB_ROOT_PASSWORD - root db password
* MONGO_INITDB_DATABASE - root db name

### mongodb_user_credentials.env
* MONGO_CONNECTION_STRING - It should be `mongodb://<USERNAME>:<PASSWORD>@<DB_ADDRESS>/<DB_NAME>`. `<DB_ADDRESS>` for local stack is just `localhost`. These values don't need to (and even shouldn't be) the same as values proviede in `mongodb_root_credentials.env`. Example: `MONGO_CONNECTION_STRING=mongodb://aquascopeuser:dummypass@localhost/aquascopedb`


### storage_credentials.env
* STORAGE_CONNECTION_STRING - value of Azure Storage Account connection string (`DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://0.0.0.0:10000/devstoreaccount1;` if using local Docker stack)

### user_authentication.env
* JWT_SECRET_KEY - key for signing JWT tokens
* AQUASCOPE_TEST_USER - username of the only user in the system
* AQUASCOPE_TEST_PASS - password of the only user in the system encoded with `pbkdf2_sha256` algorithm from `passlib` library.


## Run the stack locally with Docker
In orded to run the stack locally you need to define all required environment files and execute the following commands:
```bash
touch webserver.log
docker-compose build
docker-compose up -d
```
