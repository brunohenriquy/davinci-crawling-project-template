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
