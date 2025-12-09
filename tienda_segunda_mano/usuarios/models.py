from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=10, choices=[('comprador', 'Comprador'), ('vendedor', 'Vendedor')], default='comprador')
    telefono = models.CharField(max_length=15, blank=True, verbose_name="Teléfono")
    ubicacion = models.CharField(max_length=100, blank=True, verbose_name="Ubicación")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    imagen_perfil = models.ImageField(upload_to="perfiles", null=True, blank=True, verbose_name="Imagen de Perfil")

    def __str__(self):
        return f"{self.user.username} - {self.tipo_usuario}"


class Resena(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resenas_dadas', verbose_name="Revisor")
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resenas_recibidas', verbose_name="Usuario Revisado")
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE, related_name='resenas', verbose_name="Producto")
    comentario = models.TextField(verbose_name="Comentario")
    rating = models.IntegerField(choices=[(1, '1 estrella'), (2, '2 estrellas'), (3, '3 estrellas'), (4, '4 estrellas'), (5, '5 estrellas')], default=5, verbose_name="Calificación")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ['-created']
        constraints = [
            models.UniqueConstraint(fields=['reviewer', 'producto'], name='unique_reviewer_producto')
        ]

    def __str__(self):
        return f"Reseña de {self.reviewer.username} para {self.reviewed_user.username} - {self.rating} estrellas"
