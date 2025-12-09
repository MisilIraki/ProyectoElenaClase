from django.db import models
from ckeditor.fields import RichTextField


class Alumnos(models.Model):
    matricula = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100, blank=True, null=True)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    imagen = models.ImageField(upload_to="alumnos/", blank=True, null=True)
    carrera = models.CharField(max_length=100)
    turno = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.nombre} {self.apellido_paterno or ''} {self.apellido_materno or ''}".strip()
        )


class Comentario(models.Model):
    """
    Comentarios creados desde el panel de administración.
    Asociados a un alumno específico.
    """

    coment = RichTextField(verbose_name="Comentario")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Registrado")
    alumno = models.ForeignKey(
        Alumnos, on_delete=models.CASCADE, verbose_name="Alumno"
    )

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ["-created"]

    def __str__(self):
        return self.coment[:50] if len(self.coment) > 50 else self.coment


class ComentarioContacto(models.Model):
    """
    Comentarios de contacto creados desde el formulario web.
    No están asociados a ningún alumno específico.
    """

    usuario = models.CharField(max_length=100, verbose_name="Usuario")
    comentario = RichTextField(verbose_name="Comentario")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Registrado")

    class Meta:
        verbose_name = "Comentario contacto"
        verbose_name_plural = "Comentarios contactos"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.usuario} - {self.comentario[:30] if len(self.comentario) > 30 else self.comentario}"


class Archivos(models.Model):
    """
    Modelo para manejar la carga de archivos genéricos.
    Sigue exactamente la estructura solicitada en la actividad.
    """

    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    archivo = models.FileField(upload_to="archivos", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Archivo"
        verbose_name_plural = "Archivos"
        ordering = ["-created"]

    def __str__(self):
        return self.titulo
