from django.contrib import admin

from .models import Game

class GameAdmin(admin.ModelAdmin):
    fields = ('nombre', 'imagen', 'descripcion', 'precio', 'categoria', 'existencia')
    list_display = ('__str__', 'slug', 'precio', 'categoria', 'existencia')

admin.site.register(Game, GameAdmin)
