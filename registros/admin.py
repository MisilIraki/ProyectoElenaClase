from django.contrib import admin
from .models import Alumnos, Comentario, ComentarioContacto
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.html import strip_tags

class AdministrarModelo(admin.ModelAdmin):
    list_display = ('matricula', 'nombre', 'apellido_paterno', 'apellido_materno', 'carrera', 'turno', 'created')
    list_filter = ('carrera', 'turno', 'created')
    search_fields = ('matricula', 'nombre', 'apellido_paterno', 'apellido_materno', 'carrera')
    readonly_fields = ('created', 'updated')
    date_hierarchy = 'created'
    ordering = ('-created',)
    fields = ('imagen', 'matricula', 'nombre', 'carrera', 'turno')

    def get_readonly_fields(self, request, obj=None):
        base_readonly = ('created', 'updated')
        admin_limited_fields = ('matricula', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'carrera', 'turno',)
        if request.user.is_superuser:
            return base_readonly
        if request.user.groups.filter(name='Usuario').exists():
            return admin_limited_fields
        return base_readonly + admin_limited_fields

    

class ComentarioForm(forms.ModelForm):
    coment = forms.CharField(widget=CKEditorWidget(), label='Comentario')

    class Meta:
        model = Comentario
        fields = '__all__'

class AdministrarComentarios(admin.ModelAdmin):
    """
    Comentarios creados desde el panel de admin.
    Asociados a un alumno específico.
    """
    form = ComentarioForm
    list_display = ('alumno', 'comentario_preview', 'created')
    list_filter = ('created', 'alumno')
    search_fields = ('coment', 'alumno__nombre', 'alumno__apellido_paterno', 'alumno__matricula')
    readonly_fields = ('created',)
    date_hierarchy = 'created'
    ordering = ('-created',)
    list_per_page = 25
    
    def comentario_preview(self, obj):
        """Muestra una vista previa del comentario (primeros 50 caracteres)"""
        texto_limpio = strip_tags(obj.coment)
        return texto_limpio[:50] + '...' if len(texto_limpio) > 50 else texto_limpio
    comentario_preview.short_description = 'Comentario'

class ComentarioContactoForm(forms.ModelForm):
    comentario = forms.CharField(widget=CKEditorWidget(), label='Comentario')

    class Meta:
        model = ComentarioContacto
        fields = '__all__'

class AdministrarComentariosContacto(admin.ModelAdmin):
    """
    Comentarios de contacto creados desde el formulario web.
    Pueden ser gestionados también desde el admin.
    """
    form = ComentarioContactoForm
    list_display = ('id', 'usuario', 'comentario_preview', 'created')
    list_filter = ('created',)
    search_fields = ('usuario', 'comentario')
    readonly_fields = ('created',)
    date_hierarchy = 'created'
    ordering = ('-created',)
    list_per_page = 25
    
    def comentario_preview(self, obj):
        """Muestra una vista previa del comentario (primeros 50 caracteres)"""
        texto_limpio = strip_tags(obj.comentario)
        return texto_limpio[:50] + '...' if len(texto_limpio) > 50 else texto_limpio
    comentario_preview.short_description = 'Comentario'

admin.site.register(Alumnos, AdministrarModelo)
admin.site.register(Comentario, AdministrarComentarios)
admin.site.register(ComentarioContacto, AdministrarComentariosContacto)
