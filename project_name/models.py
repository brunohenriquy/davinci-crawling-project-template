# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 PreSeries Tech, SL

import logging
from datetime import datetime
import uuid

from caravaggio_rest_api.dse.models import CustomDjangoCassandraModel
from django.db.models.signals import pre_save
from django.dispatch import receiver

try:
    from dse.cqlengine import columns, ValidationError
except ImportError:
    from cassandra.cqlengine import columns, ValidationError

from {{ project_name }} import CRAWLER_NAME

_logger = logging.getLogger("davinci_crawler_{}.models".format(CRAWLER_NAME))

SITUATION_CANCELLED = "CANCELED"
SITUATION_GRANTED = "GRANTED"

SITUATIONS = [SITUATION_CANCELLED, SITUATION_GRANTED]


class {{ project_name|capfirst }}Resource(CustomDjangoCassandraModel):

    __table_name__ = "{{ project_name }}_resource"

    # Force that all the values will reside in the seam node of the cluster
    _id = columns.UUID(partition_key=True, default=uuid.uuid4)

    # When was created the entity and the last modification date
    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)

    # Controls if the entity is active or has been deleted
    is_deleted = columns.Boolean(default=False)
    deleted_reason = columns.Text()

    crawl_param = columns.Integer(required=True)

    name = columns.Text(required=True)

    situation = columns.Text(required=True)

    short_description = columns.Text()

    long_description = columns.Text()

    class Meta:
        get_pk_field = "_id"

    def validate(self):
        super().validate()

        if self.situation not in SITUATIONS:
            raise ValidationError(
                "Invalid situation [{0}]. Valid situations are: {1}.".
                    format(self.situation, SITUATIONS))


# We need to set the new value for the changed_at field
@receiver(pre_save, sender={{ project_name|capfirst }}Resource)
def pre_save_{{ project_name|lower }}_resource(
        sender, instance=None, using=None, update_fields=None, **kwargs):
    instance.updated_at = datetime.utcnow()
