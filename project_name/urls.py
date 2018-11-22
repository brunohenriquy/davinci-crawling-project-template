# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 PreSeries Tech, SL

"""
{{ project_name }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2./topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from rest_framework_cache.registry import cache_registry
from rest_framework.schemas import get_schema_view

from django.contrib import admin

from caravaggio_rest_api.users.urls import urlpatterns as users_urls
from caravaggio_rest_api.views import CustomAuthToken, get_swagger_view


urlpatterns = [
    # ## DO NOT TOUCH

    # Django REST Framework auth urls
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),

    # Mechanism for clients to obtain a token given the username and password.
    url(r'^api-token-auth/', CustomAuthToken.as_view()),

    # Access to the admin site
    url(r'^admin/', admin.site.urls),

    # Django Rest Framework Swagger documentation
    url(r'^schema/$',
        get_swagger_view(title='API Documentation')),

    url(r'^api-schema/users/$',
        get_schema_view(title="Uses API",
                        patterns=[url(r'^users/',
                                      include(users_urls))])),

    # Users API version
    url(r'^users/', include(users_urls)),

]

cache_registry.autodiscover()
