from django.urls import re_path, include

from .authentication.urls import urlpatterns as auth_urls
from .tasks.urls import router as tasks_router, router

v1_urlpatterns = [
    re_path(r'', include(auth_urls)),
    re_path(r'', include(router.urls)),
]