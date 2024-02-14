
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from tenant.views import Login, Logout
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/login', permanent=False)),
    path('logout', Logout.as_view(), name='logout'),
    path('login', Login.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('property/', include('properties.urls'), name='property'),
    path('tenant/', include('tenant.urls'), name='tenant')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
