from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Task, Tag
from .permissions import IsOwner, IsAdminOrReadOnly
from .schemas.schemas import task_schema, common_task_extend_schema, common_tag_extend_schema
from .serializers import TaskSerializer, TagSerializer

@common_task_extend_schema
@task_schema
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().prefetch_related('tags')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
    lookup_field = 'slug'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(methods=['get'], detail=False, url_path='tags')
    def get_by_tags(self, request):
        tags = request.query_params.getlist('tag')
        if tags:
            queryset = Task.objects.filter(tags__slug__in=tags).prefetch_related('tags')
        else:
            queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@common_tag_extend_schema
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
    lookup_field = 'slug'

