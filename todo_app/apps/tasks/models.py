from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Index

from apps.tasks.mixins import BaseModelMixin
from apps.utils import generate_custom_id, unique_slug_generator


class Tag(BaseModelMixin):
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True, default=None)
    name = models.CharField(max_length=255, verbose_name='Тег')


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, self.name)
        self.id = generate_custom_id(self.slug)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        indexes = (
            Index(fields=('slug',)),
        )

class Task(BaseModelMixin):
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True, default=None)
    title = models.CharField(max_length=255, verbose_name='Задача')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    start_datetime = models.DateTimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tasks', verbose_name='Тэги')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, self.title)
        self.id = generate_custom_id(self.slug, self.user.tg_id)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        indexes = (
            Index(fields=('slug',)),
        )