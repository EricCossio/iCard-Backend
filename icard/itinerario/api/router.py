from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvitacionViewSet, TareaViewSet

router = DefaultRouter()
router.register(r'tareas', TareaViewSet, basename='tarea')
router.register(r'invitaciones', InvitacionViewSet,  basename='invitacion')  # ← nueva

urlpatterns = [
    path('', include(router.urls)),
]