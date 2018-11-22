# Django DaVinci Crawler project template

This is a simple DaVinci project template with my preferred setup. 

This template has also support for Docker and is also optimized for Google App Engine deployments.

## Features

- Caravggio REST API Framwework (Django 2.0+, DRF, DataStax/Cassandra)
- DaVinci Crawling Framwework 
- PostgreSQL database support with psycopg2.
- DataStax database support with DSE Driver
- Development, Staging and Production settings with django-configurations.
- Get value insight and debug information while on Development with django-debug-toolbar.
- Collection of custom extensions with django-extensions.
- HTTPS and other security related settings on Staging and Production.
- Google App Engine deployment support

## How to install

```
$ django-admin.py startproject \
  --template=https://github.com/jpadilla/django-project-template/archive/master.zip \
  --name=Procfile \
  --extension=py,md,env \
  bovespa
$ mv example.env .env
$ pipenv install --dev```
```
