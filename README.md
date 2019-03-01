# aquascope_backend

## Getting started
After you clone the repo please make sure you have also pulled LFS data. If not then run the following command:
```bash
git lfs pull
```

## Environment files
Stack needs `.env` files to run. The files are filled in with some default values in the repo so you do not have to take any action here. The files are tracked by git however so if you make some local modifications to them that you do not want to push upstream please run
```bash
git update-index --skip-worktree <filepath>
```
on each changed `.env` file.

## Run the stack locally with Docker
In order to run the stack locally you need to define all required environment files and execute the following commands:

### Starting the stack
```bash
mkdir db_data
touch webserver.log
docker-compose build
docker-compose up -d
```

### Removing the stack
```bash
docker-compose stop ; docker-compose rm -v -f
```

## Running unit tests
Assuming you have already prepared python environment, in order to run unit tests ensure that you have set two variables `STORAGE_CONNECTION_STRING` and `MONGO_TEST_DB_CONNECTION_STRING`, then type in your command line `python -m unittest discover -s aquascope/tests -t .`
Ensure that you included the STORAGE_CONENCTION_STRING in quotation marks.

## Seeding database with exemplary data
If you want to seed the DB with exemplary data please make sure you have your local stack up and running and please execute the following command:
```bash
bash ./seed_db.bash
```

## Environment files description
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
* AQUASCOPE_SECONDARY_PASS - secondary password to the system encoded with `pbkdf2_sha256` algorithm from `passlib` library.
