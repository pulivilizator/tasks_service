from django.db import models

class BaseModelMixin(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True