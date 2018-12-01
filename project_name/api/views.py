# -*- coding: utf-8 -*
from drf_haystack.filters import HaystackFilter, HaystackBoostFilter, \
    HaystackGEOSpatialFilter, HaystackFacetFilter

from caravaggio_rest_api.drf_haystack.filters import \
    HaystackOrderingFilter

from caravaggio_rest_api.drf_haystack.viewsets import \
    CustomModelViewSet, CustomHaystackViewSet


# from rest_framework.authentication import \
#    TokenAuthentication, SessionAuthentication
# from rest_framework.permissions import IsAuthenticated

from drf_haystack import mixins

from .serializers import {{ project_name | capfirst }}ResourceSerializerV1, \
    {{ project_name | capfirst }}ResourceSearchSerializerV1, \
    {{ project_name | capfirst }}ResourceGEOSearchSerializerV1, \
    {{ project_name | capfirst }}ResourceFacetSerializerV1

from {{ project_name | lower }}.models import {{project_name | capfirst}}Resource


class {{ project_name | capfirst }}ResourceViewSet(CustomModelViewSet):
    queryset = {{ project_name | capfirst }}Resource.objects.all()

    # Defined in the settings as default authentication classes
    # authentication_classes = (
    #    TokenAuthentication, SessionAuthentication)

    # Defined in the settings as default permission classes
    # permission_classes = (IsAuthenticated,)

    serializer_class = {{ project_name | capfirst }}ResourceSerializerV1

    filter_fields = ("_id", "created_at", "updated_at", "situation",
                     'country_code')


class {{ project_name | capfirst }}ResourceSearchViewSet(mixins.FacetMixin, CustomHaystackViewSet):

    filter_backends = [
        HaystackFilter, HaystackBoostFilter,
        HaystackFacetFilter, HaystackOrderingFilter]

    # `index_models` is an optional list of which models you would like
    #  to include in the search result. You might have several models
    #  indexed, and this provides a way to filter out those of no interest
    #  for this particular view.
    # (Translates to `SearchQuerySet().models(*index_models)`
    # behind the scenes.
    index_models = [{{ project_name | capfirst }}Resource]

    # Defined in the settings as default authentication classes
    # authentication_classes = (
    #   TokenAuthentication, SessionAuthentication)

    # Defined in the settings as default permission classes
    # permission_classes = (IsAuthenticated,)

    serializer_class = {{ project_name | capfirst }}ResourceSearchSerializerV1

    facet_serializer_class = {{ project_name | capfirst }}ResourceFacetSerializerV1

    # The Search viewsets needs information about the serializer to be use
    # with the results. The previous serializer is used to parse
    # the search requests adding fields like text, autocomplete, score, etc.
    results_serializer_class = {{ project_name | capfirst }}ResourceSerializerV1

    ordering_fields = (
        "_id", "name", "short_description", "long_description",
        "situation", "crawl_param",
        "created_at", "updated_at")


class {{ project_name | capfirst }}ResourceGEOSearchViewSet(CustomHaystackViewSet):

    filter_backends = [
        HaystackFilter, HaystackBoostFilter,
        HaystackGEOSpatialFilter, HaystackOrderingFilter]

    # `index_models` is an optional list of which models you would like
    #  to include in the search result. You might have several models
    #  indexed, and this provides a way to filter out those of no interest
    #  for this particular view.
    # (Translates to `SearchQuerySet().models(*index_models)`
    # behind the scenes.
    index_models = [{{ project_name | capfirst }}Resource]

    # Defined in the settings as default authentication classes
    # authentication_classes = (
    #   TokenAuthentication, SessionAuthentication)

    # Defined in the settings as default permission classes
    # permission_classes = (IsAuthenticated,)

    serializer_class = {{ project_name | capfirst }}ResourceGEOSearchSerializerV1

    # The Search viewsets needs information about the serializer to be use
    # with the results. The previous serializer is used to parse
    # the search requests adding fields like text, autocomplete, score, etc.
    results_serializer_class = {{ project_name | capfirst }}ResourceSerializerV1

    ordering_fields = ("_id", "created_at", "updated_at", "foundation_date",
                       "country_code", "specialties")
