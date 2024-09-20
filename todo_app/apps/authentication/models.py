from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import Index
from django.utils import timezone

from .manager import UserManager
from .utils import generate_custom_id


class User(AbstractBaseUser):
    id = models.CharField(
        max_length=16,
        primary_key=True,
        default=generate_custom_id,
        editable=False
    )
    email = models.EmailField(max_length=255, unique=True, verbose_name='Почта')
    name = models.CharField(max_length=255, verbose_name='Имя')
    surname = models.CharField(max_length=255, verbose_name='Фамилия')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

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
        return f'{self.surname} {self.name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        indexes = (
            Index(fields=('email',)),
        )

