# -*- coding: utf-8 -*
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date

from caravaggio_rest_api.drf_haystack.serializers import \
    BaseCachedSerializerMixin

from rest_framework_cache.registry import cache_registry

from caravaggio_rest_api.drf_haystack import serializers as dse_serializers

from {{ project_name | lower }}.models import \
    MyResource


class MyResourceSerializerV1(
        dse_serializers.CassandraModelSerializer, BaseCachedSerializerMixin):
    """
    Represents a Business Object API View with support for JSON, list, and map
    fields.
    """

    class Meta:
        model = MyResource
        fields = ("id",
                  "created_at", "updated_at",
                  "name", "short_description", "long_description")
        read_only_fields = ("_id", "created_at", "updated_at")


# Cache configuration
cache_registry.register(MyResourceSerializerV1)
