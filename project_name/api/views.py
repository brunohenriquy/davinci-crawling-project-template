# -*- coding: utf-8 -*
from caravaggio_rest_api.drf_haystack.viewsets import \
    CaravaggioCassandraModelViewSet, \
    CaravaggioHaystackGEOSearchViewSet, \
    CaravaggioHaystackFacetSearchViewSet

# from rest_framework.authentication import \
#    TokenAuthentication, SessionAuthentication
# from rest_framework.permissions import IsAuthenticated

from .serializers import MyResourceSerializerV1

from {{ project_name | lower }}.models import {{ project_name | capfirst }}Resource


class {{ project_name | capfirst }}ResourceViewSet(CaravaggioCassandraModelViewSet):
    queryset = {{ project_name | capfirst }}Resource.objects.all()

    # Defined in the settings as default authentication classes
    # authentication_classes = (
    #    TokenAuthentication, SessionAuthentication)

    # Defined in the settings as default permission classes
    # permission_classes = (IsAuthenticated,)

    serializer_class = {{ project_name | capfirst }}ResourceSerializerV1
