
from django.urls import path
from .views import ManageProperty, view_agreement

urlpatterns = [
    path('', ManageProperty.as_view(), name=''),
    path('view-agreement/', view_agreement, name="view-agreement")
    # path('unit/', ManageUnit.as_view(), name='unit'),
]