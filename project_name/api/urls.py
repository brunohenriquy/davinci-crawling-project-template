"""
Company URL Configuration

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

from {{ project_name }}.api.views import \
    {{project_name | capfirst}}ResourceViewSet, {{ project_name|capfirst }}ResourceSearchViewSet

from rest_framework import routers

# API v1 Router. Provide an easy way of automatically determining the URL conf.

api_{{ project_name | upper }} = routers.DefaultRouter()

api_{{ project_name | upper }}.register(r'{{ project_name }}/search',
                        {{project_name | capfirst}}ResourceSearchViewSet,
                        base_name="{{ project_name }}-search")

api_{{ project_name | upper }}.register(r'{{ project_name }}',
                        {{project_name | capfirst}}ResourceViewSet,
                        base_name="{{ project_name }}")

urlpatterns = [
    # Company API version
    url(r'^', include(api_{{ project_name | upper }}.urls), name="{{ project_name }}-api"),
]
