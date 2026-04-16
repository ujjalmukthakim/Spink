from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("dj-admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.auth_urls")),
    path("api/users/", include("apps.accounts.urls")),
    path("api/posts/", include("apps.posts.urls")),
    path("api/tasks/", include("apps.tasks.urls")),
    path("api/admin/", include("apps.core.urls")),
]
