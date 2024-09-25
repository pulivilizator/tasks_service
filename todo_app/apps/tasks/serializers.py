from rest_framework import serializers
from .models import Tag, Task

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['slug', 'name', 'created_at']
        read_only_fields = ['id', 'slug']

class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'slug', 'user']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            task.tags.add(tag)
        return task

    def update(self, instance: Task, validated_data):
        tags_data = validated_data.pop('tags', [])
        for k, v in validated_data.items():
            if hasattr(instance, k):
                setattr(instance, k, v)
        instance.save()
        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            if tag not in instance.tags.all():
                instance.tags.add(tag)
        return instance

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['slug', 'title', 'created_at']
