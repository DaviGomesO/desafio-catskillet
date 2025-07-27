from django.contrib import admin
from tasks.models import Category, Task


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon', 'created_at')
    search_fields = ('name',)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'execution_date', 'created_at', 'updated_at', 'status', 'user')
    list_filter = ('status', 'execution_date', 'categories', 'user')
    search_fields = ('title', 'description')
    date_hierarchy = 'execution_date'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Task, TaskAdmin)
