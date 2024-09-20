from django.urls import re_path, include
from .authentication.urls import urlpatterns as auth_urls

v1_urlpatterns = [
    re_path(r'', include((auth_urls, 'authentication'))),
]