from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

print(include(wagtailadmin_urls))
print(wagtailadmin_urls.urlpatterns)

def myview(req):
    from django.urls import reverse
    from django.http import HttpResponse
    print(reverse('wagtailadmin_explore', args=['']))
    return HttpResponse('test')


urlpatterns = [
    re_path(r'^cms/', include('wagtail.admin.urls')),
    re_path(r'^test/', myview),
    # re_path(r'^cms/', wagtailadmin_urls.urlpatterns),
    # re_path(r'^documents/', include(wagtaildocs_urls)),
    # re_path(r'^pages/', include(wagtail_urls)),
    # path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
