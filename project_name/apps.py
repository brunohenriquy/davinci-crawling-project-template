# -*- coding: utf-8 -*
# Copyright (c) 2018-2019 PreSeries Tech, SL
# All rights reserved.

from django.apps import AppConfig


class DaVinciCrawlerConfig(AppConfig):
    name = '{{ project_name }}'
    verbose_name = "Django DaVinci Crawler {{ project_name }}"

    def ready(self):
        pass
        # Add System checks
        # from .checks import pagination_system_check  # NOQA
