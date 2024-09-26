from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import Index

from .manager import UserManager
from apps.utils import generate_custom_id


class User(AbstractBaseUser):
    tg_id = models.BigIntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=255, unique=True, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=128, blank=True, null=True)

    USERNAME_FIELD = 'tg_id'
    REQUIRED_FIELDS = ['username', 'first_name']

    objects = UserManager()

    def __str__(self):
        return self.full_name()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def full_name(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        indexes = (
            Index(fields=('username',)),
        )

