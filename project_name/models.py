# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 PreSeries Tech, SL

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

SITUATION_CANCELLED = "CANCELED"
SITUATION_GRANTED = "GRANTED"

SITUATIONS = [SITUATION_CANCELLED, SITUATION_GRANTED]


class {{ project_name | capfirst }}Resource(CustomDjangoCassandraModel):

    __table_name__ = "{{ project_name | lower }}_resource"

    # Force that all the values will reside in the seam node of the cluster
    _id = columns.UUID(partition_key=True, default=uuid.uuid4)

    # The owner of the data. Who own's the company data persisted
    user = columns.Text(primary_key=True)

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

    # The date when the company was founded
    foundation_date = columns.Date()

    # Country of the company
    # ISO 3166-1 alpha 3 code
    country_code = columns.Text(min_length=3, max_length=3)

    # A list of specialties of the company
    specialties = columns.List(value_type=columns.Text)

    # A field that represent a map of key-value
    # We use caravaggio KeyEncodedMap that appends the field name
    # to each of the keys in order to make them indexable by the
    # Search Indexer.
    websites = KeyEncodedMap(
        key_type=columns.Text, value_type=columns.Text)

    # A field that represents a raw JSON content
    extra_data = columns.Text()

    latitude = columns.Float()
    longitude = columns.Float()

    coordinates = columns.Text()

    class Meta:
        get_pk_field = "_id"

    def validate(self):
        super().validate()

        if self.situation not in SITUATIONS:
            raise ValidationError(
                "Invalid situation [{0}]. Valid situations are: {1}.".
                    format(self.situation, SITUATIONS))


# We need to set the new value for the changed_at field
@receiver(pre_save, sender={{ project_name | capfirst }}Resource)
def pre_save_{{ project_name | lower }}_resource(
        sender, instance=None, using=None, update_fields=None, **kwargs):
    instance.updated_at = datetime.utcnow()

    # Convert the latitude and longitude into a Geo Point in text
    # This is the field Solr understands and can index
    if instance.longitude and instance.latitude:
        instance.coordinates = "{0},{1}".format(
            instance.latitude, instance.longitude)
