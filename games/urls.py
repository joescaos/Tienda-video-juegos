from django.urls import path
from .views import GameDetailView, GameSearchListView

app_name='juego'

urlpatterns = [

    path('search', GameSearchListView.as_view(), name='search'),
    path('<slug:slug>', GameDetailView.as_view(), name='juego'),
    
]