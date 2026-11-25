from django.contrib import admin
from .models import Planeta


@admin.register(Planeta)
class PlanetaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'tipo_planeta', 'distancia', 'ano_descoberta', 'metodo_descoberta')
    list_filter = ('tipo_planeta', 'metodo_descoberta')
    search_fields = ('nome',)
