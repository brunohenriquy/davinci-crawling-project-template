# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 PreSeries Tech, SL

import logging
from django.utils import timezone

from haystack import indexes

from caravaggio_rest_api.haystack.indexes import BaseSearchIndex

from {{ project_name | lower }} import CRAWLER_NAME
from .models import {{ project_name | capfirst }}Resource

_logger = logging.getLogger("davinci_crawler_{}.search_indexes".
                            format(CRAWLER_NAME))


class {{ project_name | capfirst }}ResourceIndex(BaseSearchIndex, indexes.Indexable):

    user = indexes.CharField(
        model_attr="user")

    situation = indexes.CharField(
        model_attr="situation", faceted=True)

    crawl_param = indexes.CharField(
        model_attr="crawl_param", faceted=True)

    name = indexes.CharField(
        model_attr="name")

    short_description = indexes.CharField(
        model_attr="short_description")

    long_description = indexes.CharField(
        model_attr="long_description")

    foundation_date = indexes.DateField(
        model_attr="foundation_date", faceted=True)

    country_code = indexes.CharField(
        model_attr="country_code", faceted=True)

    coordinates = indexes.LocationField(
        model_attr="coordinates")

    specialties = indexes.MultiValueField(
        null=True, model_attr="specialties", faceted=True)

    websites = indexes.MultiValueField(
        null=True, model_attr="websites")

    extra_data = indexes.CharField(
        model_attr="extra_data")

    # When was created the entity and the last modification date
    created_at = indexes.DateTimeField(
        model_attr="created_at", faceted=True)
    updated_at = indexes.DateTimeField(
        model_attr="updated_at", faceted=True)

    is_deleted = indexes.BooleanField(
        model_attr="is_deleted", faceted=True)
    deleted_reason = indexes.CharField(
        model_attr="deleted_reason")

    class Meta:

        text_fields = ["short_description", "long_description", "extra_data"]

        # Once the index has been created it cannot be changed
        # with sync_indexes. Changes should be made by hand.
        index_settings = {
            "realtime": "true",
            "autoCommitTime": "100",
            "ramBufferSize": "2048"
        }

    def get_model(self):
        return {{ project_name | capfirst }}Resource

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            created_at__lte=timezone.now(),
            is_deleted=False
        )
