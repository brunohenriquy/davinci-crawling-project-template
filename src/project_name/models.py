# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 BuildGroup Data Services Inc.

import logging
from django.utils import timezone
import uuid

from caravaggio_rest_api.dse.models import \
    CustomDjangoCassandraModel, KeyEncodedMap
from django.db.models.signals import pre_save
from django.dispatch import receiver

try:
    from dse.cqlengine import columns, ValidationError
except ImportError:
    from cassandra.cqlengine import columns, ValidationError

from {{ project_name | lower }} import CRAWLING_PROJECT_NAME

_logger = logging.getLogger("davinci_{}.models".format(CRAWLING_PROJECT_NAME))


class {{ project_name | capfirst }}Resource(CustomDjangoCassandraModel):

    __table_name__ = "{{ project_name | lower }}_resource"

    # Force that all the values will reside in the seam node of the cluster
    id = columns.UUID(partition_key=True, default=uuid.uuid4)

    # When was created the entity and the last modification date
    created_at = columns.DateTime(default=timezone.now)
    updated_at = columns.DateTime(default=timezone.now)

    name = columns.Text(required=True)

    short_description = columns.Text()

    long_description = columns.Text()

    class Meta:
        get_pk_field = "id"

    def validate(self):
        super().validate()


# We need to set the new value for the changed_at field
@receiver(pre_save, sender={{ project_name | capfirst }}Resource)
def pre_save_{{ project_name | lower }}_resource(
        sender, instance=None, using=None, update_fields=None, **kwargs):
    instance.updated_at = timezone.now()
