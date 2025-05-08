from django.contrib import admin
from .models import Horario

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('dia', 'hora_inicio', 'descricao')  # Exibe as colunas no admin
    search_fields = ('dia', 'hora_inicio', 'descricao')  # Permite buscar pelos campos
    list_filter = ('dia',)  # Filtro para visualizar por dia