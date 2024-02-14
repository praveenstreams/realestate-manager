from django.urls import path
from .views import ManageTenant

urlpatterns = [
    path('', ManageTenant.as_view(), name=''),


]