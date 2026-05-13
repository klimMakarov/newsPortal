import django.forms
import django_filters
from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    author = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Автор'
    )

    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Заголовок'
    )

    created = django_filters.DateFilter(
        lookup_expr='gt',
        label='Опубликовано после',
        widget=django.forms.DateInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Post
        fields = []