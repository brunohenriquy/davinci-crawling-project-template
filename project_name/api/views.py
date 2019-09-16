# -*- coding: utf-8 -*
from caravaggio_rest_api.drf_haystack.viewsets import \
    CustomModelViewSet

# from rest_framework.authentication import \
#    TokenAuthentication, SessionAuthentication
# from rest_framework.permissions import IsAuthenticated

from drf_haystack import mixins

from .serializers import MyResourceSerializerV1

from {{ project_name | lower }}.models import MyResource


class MyResourceViewSet(CustomModelViewSet):
    queryset = MyResource.objects.all()

    # Defined in the settings as default authentication classes
    # authentication_classes = (
    #    TokenAuthentication, SessionAuthentication)

    # Defined in the settings as default permission classes
    # permission_classes = (IsAuthenticated,)

    serializer_class = MyResourceSerializerV1

    filter_fields = ("id", "created_at", "updated_at")
