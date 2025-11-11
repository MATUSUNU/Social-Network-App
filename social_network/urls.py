
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),  # new
    path("", Home.as_view(), name="home"),  # new
    path("groups/", include("group.urls")),  # new
    path("posts/", include("post.urls")),  # new
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
