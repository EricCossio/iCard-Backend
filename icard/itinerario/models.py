from django.db import models
from django.conf import settings  # ← usa settings en lugar de importar User directo

class Tarea(models.Model):
    CATEGORIA_CHOICES = [
        ('trabajo',    'Trabajo'),
        ('personal',   'Personal'),
        ('deporte',    'Deporte'),
        ('ejercicio',  'Ejercicio'),
        ('videojuego', 'Videojuego'),
        ('juego',      'Juego'),
        ('familiar',   'Familiar'),
        ('salud',      'Salud'),
        ('musica',     'Musica'),
        ('otro',       'Otro'),
    ]
    ESTADO_CHOICES = [
        ('pendiente',   'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada',  'Completada'),
    ]

    usuario       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tareas')
    colaboradores = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Invitacion',
        through_fields=('tarea', 'invitado'),  # ← resuelve la ambiguedad
        related_name='tareas_compartidas',
        blank=True
    )
    titulo        = models.CharField(max_length=200)
    descripcion   = models.TextField(blank=True, null=True)
    categoria     = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='trabajo')
    estado        = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha         = models.DateField()
    hora_inicio   = models.TimeField(null=True, blank=True)
    hora_fin      = models.TimeField(null=True, blank=True)
    creado_en     = models.DateTimeField(auto_now_add=True)
    actualizado_en= models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['fecha', 'hora_inicio']

    def __str__(self):
        return f"{self.titulo} ({self.fecha})"


class Invitacion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente',  'Pendiente'),
        ('aceptada',   'Aceptada'),
        ('rechazada',  'Rechazada'),
    ]

    tarea        = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='invitaciones')
    invitado     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitaciones_recibidas')
    invitado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitaciones_enviadas')
    estado       = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    creado_en    = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['tarea', 'invitado']
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.invitado_por} invito a {self.invitado} a '{self.tarea}'"