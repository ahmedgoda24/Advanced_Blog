import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    content = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    tags = django_filters.CharFilter(method='filter_tags')

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']

    def filter_tags(self, queryset, name, value):
#Because a Post can have multiple tags, and because the filter might match multiple tags per Post,
# using distinct() ensures that each Post appears only once in the results, even if multiple tags match
      return queryset.filter(tags__name__in=value.split(',')).distinct() 

