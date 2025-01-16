import django_filters

from .models import Ads


class AdsFilter(django_filters.FilterSet):
    """
    Фильтр для модели объявления
    """
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ads
        fields = ['title']