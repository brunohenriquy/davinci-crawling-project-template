# -*- coding: utf-8 -*
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date

from caravaggio_rest_api.drf_haystack.serializers import \
    BaseCachedSerializerMixin, CustomHaystackSerializer
from drf_haystack.serializers import HaystackFacetSerializer

from rest_framework import fields, serializers

from rest_framework_cache.registry import cache_registry

from caravaggio_rest_api.drf_haystack import serializers as dse_serializers

from {{ project_name }}.models import \
    {{project_name | capfirst}}Resource
from {{ project_name }}.search_indexes import \
    {{ project_name | capfirst}}ResourceIndex


class {{ project_name|capfirst }}ResourceSerializerV1(
    dse_serializers.CassandraModelSerializer, BaseCachedSerializerMixin):
    """
    Represents a Business Object API View with support for JSON, list, and map
    fields.
    """

    class Meta:
        model = {{ project_name|capfirst }}Resource
        fields = ("_id",
                  "created_at", "updated_at",
                  "name", "short_description", "long_description",
                  "situation", "crawl_param")
        read_only_fields = ("_id", "created_at", "updated_at")


class {{ project_name|capfirst }}ResourceSearchSerializerV1(
    CustomHaystackSerializer, BaseCachedSerializerMixin):
    """
    A Fast Searcher (Solr) version of the original Business Object API View
    """

    score = fields.FloatField(required=False)

    class Meta(CustomHaystackSerializer.Meta):
        model = {{ project_name|capfirst }}Resource
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [{{ project_name|capfirst }}ResourceIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = [
            "_id",
            "created_at", "cnpj", "updated_at",
            "name", "short_description", "long_description",
            "situation", "crawl_param",
            "score"]


class {{ project_name|capfirst }}ResourceFacetSerializerV1(HaystackFacetSerializer):

    # Setting this to True will serialize the
    # queryset into an `objects` list. This
    # is useful if you need to display the faceted
    # results. Defaults to False.
    serialize_objects = True

    class Meta:
        index_classes = [{{ project_name|capfirst }}Resource]
        fields = ["created_at", "updated_at", "situation"]

        field_options = {
            "situation": {},
            "created_at": {
                "start_date": datetime.now() - timedelta(days=5* 365),
                "end_date": datetime.now(),
                "gap_by": "month",
                "gap_amount": 1
            },
            "updated_at": {
                "start_date": datetime.now() - timedelta(days=5 * 365),
                "end_date": datetime.now(),
                "gap_by": "month",
                "gap_amount": 1
            },
        }


# Cache configuration
cache_registry.register({{ project_name|capfirst }}ResourceSerializerV1)
cache_registry.register({{ project_name|capfirst }}ResourceSearchSerializerV1)
