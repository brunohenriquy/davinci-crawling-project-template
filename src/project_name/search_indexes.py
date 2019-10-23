# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 BuildGroup Data Services Inc.

import logging
from django.utils import timezone

from haystack import indexes

from caravaggio_rest_api.haystack.indexes import BaseSearchIndex

from {{ project_name | lower }} import CRAWLING_PROJECT_NAME
from .models import {{ project_name | capfirst }}Resource

_logger = logging.getLogger("davinci_{}.search_indexes".format(
    CRAWLING_PROJECT_NAME))


class {{ project_name | capfirst }}ResourceIndex(
        BaseSearchIndex, indexes.Indexable):

    id = indexes.CharField(
        model_attr="id")

    name = indexes.CharField(
        model_attr="name")

    short_description = indexes.CharField(
        model_attr="short_description")

    long_description = indexes.CharField(
        model_attr="long_description")

    # When was created the entity and the last modification date
    created_at = indexes.DateTimeField(
        model_attr="created_at", faceted=True)
    updated_at = indexes.DateTimeField(
        model_attr="updated_at", faceted=True)

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
            created_at__lte=timezone.now()
        )
