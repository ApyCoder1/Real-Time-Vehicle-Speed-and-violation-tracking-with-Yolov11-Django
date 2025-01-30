from django.urls import path
from .views import SpeedRecordView
from . import views

urlpatterns = [
    path('speed-records/', SpeedRecordView.as_view(), name='speed-records'),
    path('list', views.speed_records, name='speed_records'),  # URL for viewing records
    path('', views.dashboard, name='dashboard'),
]

