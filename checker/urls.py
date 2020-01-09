from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import ListView

from checker.views import StatsView
from . import views
from .models import CheckPlace

urlpatterns = [
    path('', login_required(ListView.as_view(model=CheckPlace,)), name='list_check_place'),
    path('add_check/<int:pk>', login_required(views.add_check), name='add_check'),
    path('display/<str:token_screen>', views.screen, name='screen'),
    path('stats/<int:checkplace>', views.stats, name='stats')
]