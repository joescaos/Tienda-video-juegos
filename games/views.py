from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Game
from django.db.models import Q

# Create your views here.

class GameListView(ListView):
    template_name = 'index.html'
    model = Game

class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print(context)

        return context

class GameSearchListView(ListView):
    template_name = 'games/search.html'
    model = Game.objects.all()

    def get_queryset(self):
        query = self.request.GET.get('q')

        object_list = Game.objects.filter(
            Q(nombre__icontains = query) | Q(precio__icontains = query) | Q(categoria__icontains = query)
        )
        return object_list



    

