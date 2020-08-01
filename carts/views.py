from django.shortcuts import render, redirect, get_object_or_404

from .models import Cart 
from .utils import get_or_create_cart  

from games.models import Game
from .models import CartGames

def cart(request):

    cart = get_or_create_cart(request)    

    return render(request, 'carts/cart.html', {
        'cart': cart,
    })

def add(request):
    cart = get_or_create_cart(request)
    game = get_object_or_404(Game, pk=request.POST.get('game_id'))
    quantity = int(request.POST.get('quantity', 1))

    #cart.games.add(game, through_defaults={
    #    'quantity': quantity
    #})

    cart_games = CartGames.objects.create_or_update_quantity(cart=cart, 
                                                                game=game, 
                                                                quantity=quantity
                                                            )

    return render(request, 'carts/add.html', {
        'game': game,
    })

def remove(request):
    cart = get_or_create_cart(request)
    game = get_object_or_404(Game, pk=request.POST.get('game_id'))

    cart.games.remove(game)

    return redirect('carts:cart')

