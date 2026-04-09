from users.api.serializer import UserSerializer
from rest_framework import serializers
from itinerario.models import Invitacion, Tarea

class TareaSerializer(serializers.ModelSerializer):
    es_propia = serializers.SerializerMethodField() 
    
    class Meta:
        model = Tarea
        fields = [
            'id',
            'titulo',
            'descripcion',
            'categoria',
            'estado',
            'fecha',
            'hora_inicio',
            'hora_fin',
            'creado_en',
            'actualizado_en',
            'es_propia'  # Campo calculado para indicar si es tarea propia o invitada
        ]
        # Estos campos los genera Django solo, el usuario no los manda
        read_only_fields = ['creado_en', 'actualizado_en', 'es_propia']
    def get_es_propia(self, obj):
        request = self.context.get('request')
        if request:
            return obj.usuario == request.user
        return True  # Si no hay request, asumimos que es propia (aunque no debería pasar)
        
class InvitacionSerializer(serializers.ModelSerializer):
    invitado_info    = UserSerializer(source='invitado', read_only=True)
    invitado_por_info= UserSerializer(source='invitado_por', read_only=True)
    tarea_titulo     = serializers.CharField(source='tarea.titulo', read_only=True)

    class Meta:
        model  = Invitacion
        fields = ['id', 'tarea', 'tarea_titulo', 'invitado', 'invitado_info',
                  'invitado_por', 'invitado_por_info', 'estado', 'creado_en']
        read_only_fields = ['invitado_por', 'creado_en']