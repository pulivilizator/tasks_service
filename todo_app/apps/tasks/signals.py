from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Task


@receiver(pre_delete, sender=Task)
def delete_unused_tags(sender, instance, **kwargs):
    tags = instance.tags.all()
    for tag in tags:
        if tag.tasks.count() == 1:
            tag.delete()