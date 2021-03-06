from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from church import views
from search import views as search_views


urlpatterns = [
    url(r"^django-admin/", admin.site.urls),
    url(r"^admin/", include(wagtailadmin_urls)),
    url(r"^documents/", include(wagtaildocs_urls)),
    url(r"^search/$", search_views.search, name="search"),
    path("chat/", include("chat.urls")),
    path("church/", include("church.urls")),
    path("comments/", include("comments.urls")),
    path("prayer/", include("prayer.urls")),
    path("prayer-requests/", views.prayer_requests_page, name="prayer_requests_page"),
    path("profile/", views.profile, name="profile"),
    url(
        r"^login/$",
        auth_views.LoginView.as_view(template_name="admin/login.html"),
        name="login",
    ),
    url(r"^logout/$", auth_views.LogoutView.as_view(), name="logout"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r"", include(wagtail_urls)),
]
