from django.db import models  # ← corregido, no de icard_django
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from itinerario.models import Invitacion, Tarea
from .serializer import InvitacionSerializer, TareaSerializer
from django.db.models import Q

class TareaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TareaSerializer

    def get_queryset(self):
        user = self.request.user
        # Tareas propias + tareas donde fue invitado y aceptó
        return Tarea.objects.filter(
            Q(usuario=user) |
            Q(invitaciones__invitado=user, invitaciones__estado='aceptada')
        ).distinct()  # ← distinct() evita duplicados

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


# ── Clase separada para invitaciones ──────────────────────
class InvitacionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InvitacionSerializer  # ← solo InvitacionSerializer aquí

    def get_queryset(self):
        return Invitacion.objects.filter(
            models.Q(invitado=self.request.user) |
            models.Q(invitado_por=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(invitado_por=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        invitacion = self.get_object()
        if invitacion.invitado != request.user:
            return Response({'error': 'No tienes permiso'}, status=403)
        return super().partial_update(request, *args, **kwargs)