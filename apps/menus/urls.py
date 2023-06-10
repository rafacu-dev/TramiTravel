from django.urls import path
from .views import Service,Services,Contact, download_apk

urlpatterns = [
    path('<slug:tag>/', Service.as_view(),name="service"),
    path('all/<slug:tag>/', Services.as_view(),name="services"),
    path('contact', Contact.as_view(),name="contact"),
    path('descargar-apk', download_apk, name='descargar_apk'),
]
