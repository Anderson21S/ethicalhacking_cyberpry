from django.db import models

class Incident(models.Model):
    # Opciones de severidad requeridas por la guía
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    title = models.CharField(max_length=200, blank=False)  # Título, máximo 200 caracteres, obligatorio [cite: 72]
    description = models.TextField()  # Descripción completa del incidente [cite: 72]
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)  # Opciones: Low/Medium/High/Critical [cite: 72]
    reported_at = models.DateTimeField(auto_now_add=True)  # Se establece automáticamente al crear [cite: 72]
    updated_at = models.DateTimeField(auto_now=True)  # Se actualiza automáticamente en cada cambio [cite: 72]
    resolved = models.BooleanField(default=False)  # Estado de resolución, por defecto False [cite: 72]

    def __str__(self):
        return self.title