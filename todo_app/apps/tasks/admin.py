from django.contrib import admin
from .models import Tag, Task

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('name', 'created_at', 'updated_at')
    ordering = ('name',)
    readonly_fields = ('id', 'slug', 'created_at', 'updated_at',)

    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'user__email')
    list_filter = ('user', 'tags', 'created_at', 'updated_at',)
    ordering = ('-id',)
    filter_horizontal = ('tags',)
    readonly_fields = ('id', 'slug', 'created_at', 'updated_at')
    autocomplete_fields = ['user']

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'user', 'tags')
        }),
    )

