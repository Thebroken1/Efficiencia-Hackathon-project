from django.urls import path
from . import views

urlpatterns = [
    path('', views.heatmap_view, name='heatmap'),
    path('api/heatmap_data/', views.heatmap_data, name='heatmap_data'),
]