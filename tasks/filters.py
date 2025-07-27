from django_filters import rest_framework as filters
from tasks.models import Task


# class CharInFilter(filters.BaseInFilter, filters.CharFilter):
#   """Permite filtrar pelo nome de várias categorias separadas por vírgula."""
#   pass


class TaskFilter(filters.FilterSet):
    execution_date = filters.DateFilter(field_name='execution_date')
    status = filters.ChoiceFilter(field_name='status', choices=Task.STATUS)
    categories = filters.CharFilter(field_name='categories__name', lookup_expr='icontains', label='Categoria')
    # categories = CharInFilter(field_name='categories__name', lookup_expr='in')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    # Filtros que aceita na URL
    class Meta:
        model = Task
        fields = ['title', 'description', 'execution_date', 'status', 'categories']
