from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm

    list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_admin', 'created_at')
    list_filter = ('is_active', 'is_admin', 'created_at')

    fieldsets = [
        ('User info', {
            'fields': [
                'tg_id', 'username', 'first_name', 'last_name', 'is_active'
            ],
        }),
        ('Permissions', {
            'fields': [
                'is_admin',
            ],
        }),
    ]

    add_fieldsets = [
        (None, {
            'fields': [
                'tg_id', 'username', 'first_name', 'last_name', 'password1', 'password2'
            ],
        }),
    ]

    ordering = ('username',)

    filter_horizontal = ()
