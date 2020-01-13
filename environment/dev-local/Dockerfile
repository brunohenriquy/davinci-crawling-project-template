FROM bgds/base-davinci:0.1

# DB connection information
ENV DB_USER {{ project_name | lower }}
ENV DB_PASSWORD {{ project_name | lower }}
ENV DB_NAME {{ project_name | lower }}

# CASSANDRA connection information
ENV CASSANDRA_DB_NAME {{ project_name | lower }}

RUN mkdir /{{ project_name | lower }}

ADD . /{{ project_name | lower }}/

RUN pip install Cython django-haystack

RUN cd /{{ project_name | lower }} \
    && python setup.py develop \
    && pip install django_caravaggio_rest_api[spatial] \
    && pip install -r requirements.txt || echo "ignore error" \
    && pip install -r requirements_tests.txt || echo "ignore error"

RUN mkdir -p /data/{{ project_name | lower }}/log

WORKDIR /{{ project_name | lower }}

VOLUME /{{ project_name | lower }}

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]