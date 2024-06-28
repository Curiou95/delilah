import django_filters
from django_filters import DateFilter, CharFilter

from .models import *


class BabiesFilter(django_filters.FilterSet):
    # nme = CharFilter(
    #     field_name="b_name", lookup_expr="icontains", label="search by baby name"
    # )

    class Meta:
        model = Baby
        fields = ['b_name']


class SitterFilter(django_filters.FilterSet):
    name = CharFilter(
        field_name="s_name", lookup_expr="icontains", label="search by sitter name"
    )

    class Meta:
        model = Sitter
        fields = []
