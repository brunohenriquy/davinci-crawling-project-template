# -*- coding: utf-8 -*
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date

from caravaggio_rest_api.drf_haystack.serializers import \
    BaseCachedSerializerMixin

from rest_framework_cache.registry import cache_registry

from caravaggio_rest_api.drf_haystack import serializers as dse_serializers

from {{ project_name | lower }}.models import \
    {{ project_name | capfirst }}Resource


class {{ project_name | capfirst }}ResourceSerializerV1(
        dse_serializers.CassandraModelSerializer, BaseCachedSerializerMixin):
    """
    Represents a Business Object API View with support for JSON, list, and map
    fields.
    """

    class Meta:
        model = {{ project_name | capfirst }}Resource
        fields = ("id",
                  "created_at", "updated_at",
                  "name", "short_description", "long_description")
        read_only_fields = ("_id", "created_at", "updated_at")

        extra_kwargs = {
            'id': {
                'help_text': 'the id that is the unique partition key.'
            },
            'created_at': {
                'help_text': 'the date of the creation of the object.'
            },
            'updated_at': {
                'help_text': 'the date that we last updated the object.'
            },
            'name': {
                'help_text': 'the name of the object.'
            },
            'short_description': {
                'help_text': 'a short description of the object.'
            },
            'long_description': {
                'help_text': 'a long description of the object'
            },
        }


# Cache configuration
cache_registry.register({{ project_name | capfirst }}ResourceSerializerV1)
