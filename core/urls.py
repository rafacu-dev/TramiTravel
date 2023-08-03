import re
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static, serve
from django.conf import settings

from apps.user.views import Login, Logout, Register, RegisterConfirm, RecreatePassword, RecreateConfirm


def staticProduction(prefix, view=serve, **kwargs):
    if settings.DEBUG:
        return []
    return [
        re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs),
    ]

urlpatterns = [
    path('logout/', Logout.as_view(),name='logout'),
    path('login/', Login.as_view(),name='login'),
    path('register/', Register.as_view(),name='register'),
    path('recreate-password/', RecreatePassword.as_view(),name='recreate_password'),
    path('register-confirm/', RegisterConfirm.as_view(),name='register_confirm'),
    path('recreate-confirm/', RecreateConfirm.as_view(),name='register_confirm'),
    path('admin/', admin.site.urls),
    
    path('', include('apps.user.urls')),
    path('', include('apps.location.urls')),
    path('', include('apps.reservations.urls')),
    path('', include('apps.hotels.urls')),
    path('refills/', include('apps.refills.urls')),
    path('service/', include('apps.menus.urls')),
    path('remote-control/', include('apps.bot.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticProduction(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)