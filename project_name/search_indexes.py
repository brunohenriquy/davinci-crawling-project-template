# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 PreSeries Tech, SL

import logging
from django.utils import timezone

from haystack import indexes

from caravaggio_rest_api.indexes import BaseSearchIndex

from {{ project_name }} import CRAWLER_NAME
from .models import {{ project_name }}Resource

_logger = logging.getLogger("davinci_crawler_{}.search_indexes".
                            format(CRAWLER_NAME))


class {{ project_name }}ResourceIndex(BaseSearchIndex, indexes.Indexable):

    situation = indexes.CharField(
        model_attr="situation", faceted=True)

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

    is_deleted = indexes.BooleanField(
        model_attr="is_deleted", faceted=True)
    deleted_reason = indexes.CharField(
        model_attr="deleted_reason")

    class Meta:

        text_fields = ["short_description", "long_description"]

        # Once the index has been created it cannot be changed
        # with sync_indexes. Changes should be made by hand.
        index_settings = {
            "realtime": "true",
            "autoCommitTime": "100",
            "ramBufferSize": "2048"
        }

    def get_model(self):
        return {{ project_name }}Resource

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            created_at__lte=timezone.now(),
            is_deleted=False
        )
