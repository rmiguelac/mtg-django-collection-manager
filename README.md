# Binder manager

Binder manager is a Django lab application which provides and API to manage Magic the Gathering collections.

While it is still in the early development phases, it already consumes an external API to evaluate the cards.


### --- API Setup

To start using the application, make sure you have at least python 3.6 installed

Once you're set with python, there are a few steps to setup the application and run it.

1 - Clone the repository
```commandline
git clone git@github.com:rmiguelac/mtg-django-collection-manager.git
```

2 - Setup a virtual environment - make sure the path is python3.6
```commandline
mkdir mtg_collection && cd mtg_collection
virtualenv --python=/usr/bin/python3.6 .
```

3 - put the DJANGO_SECRET in the activate script to always have it when you start the env

Make sure you do not use only one '>' because if you do, the bin/active will be overwritten and a new virtualenv will
need to be created
```commandline
echo "export DJANGO_SECRET='your_secret_here'" >> bin/activate
```

4 - install all the requirements 
```commandline
source bin/activate
pip install -r requirements.txt
```

### --- Postgres setup

To setup postgres, make sure you have docker installed.

1 - Create a directory to persis the data
```commandline
mkdir ~/some/randon/path/to/persist/dir
```

2 - Run docker cli with the following arguments - This will download the postgres:9.6 image if you do not have it already
```commandline
docker run -d --name binder-postgres -e POSTGRESS_PASSWORD=xxxxx \
           -p 5432:5432 -v /dir/that/you/created/above:/var/lib/postgresql/data \
            postgres:9.6
```

3 - Now that you have it running, we need to create the database the API will use:

3.1 - Connect to the docker container
```commandline
docker exec -ti binder-postgres /bin/bash
```

3.2 - Change user and connect to the db
```commandline
su - postgres
psql
```

3.3 - Create the database and all roles/users that are required.
```commandline
CREATE DATABASE collection;
CREATE USER myuser WITH PASSWORD 'mypassword';
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE collection TO myuser;
```
[reference](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)

3.4 - Lastly, to run the tests, a new database should be created or django should be able to create it all alone

To do it, also execute the following with psql
```commandline
ALTER USER myuser CREATEDB;
```

### --- Running the application

```commandline
./manage.py makemigrations
./manage.py migrate
./manage.py runserver
```

### --- Running tests

[running tests](https://github.com/rmiguelac/mtg-django-collection-manager/blob/master/collection_app/tests/README.md)