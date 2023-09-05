from django.urls import path
from .views import (Pay)#,getStatesView,getCitiesView

urlpatterns = [
    path('pay/', Pay.as_view(),name='Pay'),
    
    #path('api/states/<str:name>/', getStatesView,name="states"),
    #path('api/cities/<str:cuntry>/<str:state_name>/', getCitiesView,name="cities"),
]