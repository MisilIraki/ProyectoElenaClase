from django.contrib import admin
from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_usuario', 'telefono', 'ubicacion')
    list_filter = ('tipo_usuario', 'ubicacion')
    search_fields = ('user__username', 'user__email', 'telefono', 'ubicacion')


# Personalización global del admin
admin.site.site_header = "SecondChance - Administración"
admin.site.site_title = "SecondChance | Panel de administración"
admin.site.index_title = "Panel de control de SecondChance"
