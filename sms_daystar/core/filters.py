import django_filters
from django_filters import DateFilter, CharFilter

from .models import *


class BabiesFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name='b_date', lookup_expr='gte')
    # end_date = DateFilter(field_name='b_date', lookup_expr='lte')
    nme = CharFilter(field_name='b_name',lookup_expr='icontains', label='search by baby name' )
    class Meta:
        model = Baby
        fields = [
        'b_date'
        ]


class SitterFilter(django_filters.FilterSet):
    name = CharFilter(field_name='s_name',lookup_expr='icontains', label='search by sitter name' )
    class Meta:
        model = Sitter
        fields = [
        ]