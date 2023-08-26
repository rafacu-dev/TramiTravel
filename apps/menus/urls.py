from django.urls import path
from .views import Service,Services,Contact,Form, download_apk, getCountriesView, getStatesView,getCitiesView

urlpatterns = [
    path('<slug:tag>/', Service.as_view(),name="service"),
    path('all/<slug:tag>/', Services.as_view(),name="services"),
    path('contact', Contact.as_view(),name="contact"),
    path('forms/<slug:form_name>/', Form.as_view(),name="forms"),
    path('descargar-apk', download_apk, name='descargar_apk'),
    
    path('countries/all/', getCountriesView,name="countries"),
    path('api/states/<slug:name>/', getStatesView,name="states"),
    path('api/cities/<slug:cuntry>/<slug:state_name>/', getCitiesView,name="cities"),
]
