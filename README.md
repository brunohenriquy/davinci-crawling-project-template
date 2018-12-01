# Django DaVinci Crawler project template

This is a simple DaVinci project template with my preferred setup. 

This template has also support for Docker and is also optimized for Google App Engine deployments.

## Features

- Caravaggio REST API Framework (Django 2.0+, DRF, DataStax/Cassandra)
- DaVinci Crawling Framwework 
- PostgreSQL database support with psycopg2.
- DataStax database support with DSE Driver
- Development, Staging and Production settings with django-configurations.
- Get value insight and debug information while on Development with django-debug-toolbar.
- Collection of custom extensions with django-extensions.
- HTTPS and other security related settings on Staging and Production.
- Google App Engine deployment support


## Environment Setup

We need to prepare the environment to install and execute the crawler.

We need to install, configure and start the following services:
 
- DataStax Enterprise 6.x
- PostgreSQL 9.6
- Redis 3

To do that we can follow the instructions [here](https://github.com/preseries/django-caravaggio-rest-api/blob/master/docs/local_environment.md). 

Once the previous services are ready, we can proceed with the installation.

## How to create a new project

Follow the next instructions to create a new crawler based on this project template:

```
$ conda create -n myproject pip python=3.7
$ conda activate myproject

$ pip install django>=2

$ django-admin.py startproject \
  --template=https://github.com/preseries/davinci-crawling-template-project/archive/master.zip \
  --name=Dockerfile \
  --extension=py,md,env,sh,template,yamltemplate \
  myproject
  
$ cd myproject

$ python setup.py develop
```

__NOTE__: by default we are using the `dse-driver` to connect to cassandra or DataStax Enterprise. If you want to use `cassandra-driver` edit `setup.py` and change the dependency.

__NOTE__: the installation of the dependencies will take some time because the `dse-driver` or `cassandra-driver` has to be compiled.


### Test crawler

If you want to use the Bovespa test crawler that comes with `davinci-crawling`, you should edit the `settings.py file and add davinci_crawling.example.bovespa` to the list of `INSTALLED_APPS`, just after the `davinci_crawling` application.

```python
# Application definition
INSTALLED_APPS = [
    'django_cassandra_engine',
    'django_cassandra_engine.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',

    'django_extensions',
    'debug_toolbar',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_cache',
    'rest_framework_swagger',

    'haystack',
    'caravaggio_rest_api',
    'davinci_crawling',
    'davinci_crawling.example.bovespa',
    'myproject'
]
```


### Setup the databases

Follow the instructions [here](https://github.com/preseries/django-caravaggio-rest-api/blob/master/docs/local_environment.md) to prepare your backend for development.

In this step we are going to populate the databases and its tables. The default database is a PostgreSQL (you can change it) and then we also have the cassandra database, that can be a Cassandra or DSE server.

You can change the SQL server editing the dependencies in the `setup.py` and changing the `psycopg2-binary` library by the one that contains the drivers to connect to your backend. You should configure the connection in the `DATABASES` parameter of the `settings.py` of the project. 

Once the database services are ready, we can populate the database and its tables running the following instruction:

```
$ python manage.py migrate

Operations to perform:
  Apply all migrations: admin, auth, authtoken, contenttypes, sites
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying authtoken.0001_initial... OK
  Applying authtoken.0002_auto_20160226_1747... OK
  Applying sites.0001_initial... OK
  Applying sites.0002_alter_domain_unique... OK
  ```

Populate the DataStax Enterprise (DSE) or Cassandra database:

```
$ python manage.py sync_cassandra

Creating keyspace myproject [CONNECTION cassandra] ..
Syncing django_cassandra_engine.sessions.models.Session
Syncing davinci_crawling.models.Checkpoint
Syncing myproject.models.MyprojectResource
```

Populate the DataStax Enterprise (DSE) search indexes. This feature is only available for a DSE configuration:

```
$ python manage.py sync_indexes

INFO Creating indexes in myproject4 [CONNECTION cassandra] ..
INFO Creating index %s.%s
INFO Index class associated to te model myproject.models.MyprojectResourceIndex
INFO Creating SEARCH INDEX if not exists for model: <class 'django_cassandra_engine.models.MyprojectResource'>
INFO Setting index parameters: realtime = true
INFO Setting index parameters: autoCommitTime = 100
INFO Setting index parameters: ramBufferSize = 2048
INFO Processing field field <class 'haystack.fields.CharField'>(situation)
WARNING Maybe te field has been already defined in the schema. Cause: Error from server: code=2200 [Invalid query] message="The search index schema is not valid because: Can't load schema schema.xml: [schema.xml] Duplicate field definition for 'situation' [[[situation{type=StrField,properties=indexed,omitNorms,omitTermFreqAndPositions}]]] and [[[situation{type=StrField,properties=indexed,stored,omitNorms,omitTermFreqAndPositions}]]]"
INFO Processing field field <class 'haystack.fields.CharField'>(name)
WARNING Maybe te field has been already defined in the schema. Cause: Error from server: code=2200 [Invalid query] message="The search index schema is not valid because: Can't load schema schema.xml: [schema.xml] Duplicate field definition for 'name' [[[name{type=StrField,properties=indexed,omitNorms,omitTermFreqAndPositions}]]] and [[[name{type=StrField,properties=indexed,stored,omitNorms,omitTermFreqAndPositions}]]]"
INFO Processing field field <class 'haystack.fields.CharField'>(short_description)
WARNING Maybe te field has been already defined in the schema. Cause: Error from server: code=2200 [Invalid query] message="The search index schema is not valid because: Can't load schema schema.xml: [schema.xml] Duplicate field definition for 'short_description' [[[short_description{type=StrField,properties=indexed,omitNorms,omitTermFreqAndPositions}]]] and [[[short_description{type=TextField,properties=indexed,tokenized,stored}]]]"
INFO Changing SEARCH INDEX field short_description to TextField
INFO Processing field field <class 'haystack.fields.CharField'>(long_description)
WARNING Maybe te field has been already defined in the schema. Cause: Error from server: code=2200 [Invalid query] message="The search index schema is not valid because: Can't load schema schema.xml: [schema.xml] Duplicate field definition for 'long_description' [[[long_description{type=StrField,properties=indexed,omitNorms,omitTermFreqAndPositions}]]] and [[[long_description{type=TextField,properties=indexed,tokenized,stored}]]]"
...
...
```

### Generatic the static files

We have some django extensions and the debug toolbar installed in DEBUG mode. In order to them work we need to generate the static files.

```
$ python manage.py collectstatic
``` 

The output should be something like:

```
You have requested to collect static files at the destination
location as specified in your settings:

    /...../myproject/static

This will overwrite existing files!
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: yes

0 static files copied to '/..../myproject/static', 184 unmodified.
```

### Setup the admin user

Let's create the admin user with its own auth token

```
$ python manage.py createsuperuser --username _{{ project_name }} --email {{ project_name }}@preseries.com --noinput
$ python manage.py changepassword _{{ project_name }}
Changing password for user '_{{ project_name }}'
Password: 
```

A token will be created automatically for the user. We can get it back using the following request:

```
$ curl -H "Content-Type: application/json" -X POST \
    -d '{"username": "_{{ project_name }}", "password": "MY_PASSWORD"}' \
    http://127.0.0.1:8001/api-token-auth/
    
{"token":"b10061d0b62867d0d9e3eb4a8c8cb6a068b2f14a","user_id":1,"email":"{{ project_name }}@preseries.com"}    
```

## Run the crawler

Before start the crawler we need to have ready the responses for the following questions:

- The name of our crawler. Ex. `my_crawler`

- Where is located the binary of the PhantomJS library in our local system? Ex. `/servers/phantomjs-2.1.1-macosx/bin/phantomjs`

- Where is the place in our local filesystem that is goin to be used as local - volatile - cache? Ex. `fs:///data/harvest/local`

- We are going to use Google Storage as permanent storage for our permanent cache? If yes, then we need to know the google project. Ex. `centering-badge-212119`

- The location we will use as permanent storage for our permanent cache. Ex. `gs://my_crawler_cache`

- How many workers we are going to start? Ex. `10`


After responde these questions we are ready to run the crawler: 

```
python manage.py crawl myproject \
    --workers-num 10 \
    --phantomjs-path /servers/phantomjs-2.1.1-macosx/bin/phantomjs \
    --io-gs-project centering-badge-212119 \
    --cache-dir "gs://my_crawler_cache" \
    --local-dir "fs:///data/my_crawler/local"
```

