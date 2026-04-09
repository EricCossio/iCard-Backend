from django.contrib import admin
from .models import Invitacion, Tarea

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'estado', 'fecha', 'hora_inicio']
    list_filter = ['categoria', 'estado', 'fecha']
    search_fields = ['titulo']
    
@admin.register(Invitacion)
class InvitacionAdmin(admin.ModelAdmin):
    list_display  = ['tarea', 'invitado', 'invitado_por', 'estado', 'creado_en']
    list_filter   = ['estado']