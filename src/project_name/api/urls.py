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

from {{ project_name | lower }}.api.views import \
    {{ project_name | capfirst }}ResourceViewSet

from caravaggio_rest_api.drf.routers import CaravaggioRouter

# API v1 Router. Provide an easy way of automatically determining the URL conf.

api_CRAWLER_PROJECT = CaravaggioRouter()

api_CRAWLER_PROJECT.register(r'{{ project_name | lower }}resource',
                             {{ project_name | capfirst }}ResourceViewSet,
                             base_name="{{ project_name | lower }}resource")

urlpatterns = [
    # API version
    url(r'^', include(api_CRAWLER_PROJECT.urls),
        name="{{ project_name | lower }}-api"),
]
