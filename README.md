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
$ conda create -n my_project pip python=3.7
$ conda activate my_project

$ pip install django>=2

$ django-admin.py startproject \
  --template=https://github.com/preseries/davinci-crawling-template-project/archive/master.zip \
  --name=Dockerfile \
  --extension=py,md,env,sh,template,yamltemplate \
  er
  
$ cd my_project

$ python setup.py develop
```

After create the project skeleton, we will need to populate the databases, the default and the cassandra databases.

Check the following [documentation](https://github.com/preseries/django-caravaggio-rest-api/blob/master/docs/local_environment.md) to know how to setup your DB environment.

```
$ python manage.py migrate

Operations to perform:
  Apply all migrations: admin, auth, authtoken, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying authtoken.0001_initial... OK
  Applying authtoken.0002_auto_20160226_1747... OK  
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
  Applying sites.0001_initial... OK
  Applying sites.0002_alter_domain_unique... OK
  Applying sessions.0001_initial... OK
```

Now we can create the DSE model

```
$ python manage.py sync_cassandra

Creating keyspace caravaggio [CONNECTION cassandra] ..
Syncing example.models.ExampleModel
```

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
python manage.py crawl my_crawler -v 0 --workers-num 10 --phantomjs-path /servers/phantomjs-2.1.1-macosx/bin/phantomjs  --io-gs-project centering-badge-212119 --cache-dir "gs://my_crawler_cache" --local-dir "fs:///data/my_crawler/local"
```

python manage.py crawl my_project2 -v 0 --workers-num 10 --phantomjs-path /accounts/PreSeries/servers/phantomjs-2.1.1-macosx/bin/phantomjs  --io-gs-project centering-badge-212119 --cache-dir "gs://my_project2_cache" --local-dir "fs:///data/my_project2/local"
