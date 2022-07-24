from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('create', views.create),
    path('balance', views.balance),
    path('transfer', views.transfer),
    path('history', views.history),
]
