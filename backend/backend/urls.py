from django.contrib import admin
from django.urls import path
from weather.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/home/<str:location>/', Home),
    path('api/forecast/<str:location>/', Forecast),
]
