# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 BuildGroup Data Services Inc.

import logging
from datetime import datetime
import uuid

from caravaggio_rest_api.dse.models import \
    CustomDjangoCassandraModel, KeyEncodedMap
from django.db.models.signals import pre_save
from django.dispatch import receiver

try:
    from dse.cqlengine import columns, ValidationError
except ImportError:
    from cassandra.cqlengine import columns, ValidationError

from {{ project_name | lower }} import CRAWLER_NAME

_logger = logging.getLogger("davinci_crawler_{}.models".format(CRAWLER_NAME))


class MyResource(CustomDjangoCassandraModel):

    __table_name__ = "myresource"

    # Force that all the values will reside in the seam node of the cluster
    id = columns.UUID(partition_key=True, default=uuid.uuid4)

    # When was created the entity and the last modification date
    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)

    name = columns.Text(required=True)

    short_description = columns.Text()

    long_description = columns.Text()

    class Meta:
        get_pk_field = "id"

    def validate(self):
        super().validate()


# We need to set the new value for the changed_at field
@receiver(pre_save, sender=MyResource)
def pre_save_{{ project_name | lower }}_resource(
        sender, instance=None, using=None, update_fields=None, **kwargs):
    instance.updated_at = datetime.utcnow()
