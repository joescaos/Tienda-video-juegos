from django.db import models

from users.models import User
from games.models import Game
from django.db.models.signals import pre_save, m2m_changed, post_save
import uuid
import decimal

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game, through='CartGames')
    total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

    def update_totals(self):
        self.total = sum([ 
           cg.quantity * cg.game.precio for cg in self.games_related()
         ])
        self.save()

    def games_related(self):
        return self.cartgames_set.select_related('game')

class CartGamesManager(models.Manager):

    def create_or_update_quantity(self, cart, game, quantity=1):
        object, created = self.get_or_create(cart=cart, game=game)

        if not created:
            quantity = object.quantity + quantity

        object.update_quantity(quantity)
        return object

class CartGames(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CartGamesManager()

    def update_quantity(self, quantity=1):
        self.quantity = quantity
        self.save()
    
def set_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())

def update_totals(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_totals()

def post_save_update_total(sender, instance, *args, **kwargs):
    instance.cart.update_totals()


pre_save.connect(set_cart_id, sender=Cart)
post_save.connect(post_save_update_total, sender=CartGames)
m2m_changed.connect(update_totals, sender=Cart.games.through)
