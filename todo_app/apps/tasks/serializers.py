from rest_framework import serializers
from .models import Tag, Task

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'slug', 'name']
        read_only_fields = ['id', 'slug']

class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'slug', 'title', 'description', 'start_datetime', 'user', 'tags']
        read_only_fields = ['id', 'slug', 'user']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            task.tags.add(tag)
        return task
