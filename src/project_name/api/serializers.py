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


# Cache configuration
cache_registry.register({{ project_name | capfirst }}ResourceSerializerV1)
