from django.urls import path

from . import views


urlpatterns = [
    path('search/', views.SummonerSearchFormView.as_view(), name='search'),
]
