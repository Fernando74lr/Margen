from django.urls import path
from . import views

urlpatterns = [
    # Report
    path('reports/', views.reports, name='reports'),
    path('reports/clients', views.get_clients, name='clients'),
    path('reports/clients/results', views.clients_report, name='results'),
]