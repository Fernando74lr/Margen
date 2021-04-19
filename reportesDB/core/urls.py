from django.urls import path
from . import views

urlpatterns = [
    # Core
    path('', views.home, name='home')
]