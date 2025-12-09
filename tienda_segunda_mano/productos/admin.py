from django.contrib import admin
from django import forms
from django.core.exceptions import PermissionDenied
from .models import Producto
import json


class ProductoAdminForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

    class Media:
        js = ('js/admin_producto_subcats.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categoria = None
        if self.data.get('categoria'):
            categoria = self.data.get('categoria')
        elif self.instance and self.instance.pk:
            categoria = self.instance.categoria
        subs = Producto.SUBCATEGORIAS.get(categoria, [])
        self.fields['subcategoria'].choices = [('', '---------')] + subs
        # Pasamos el mapping al widget para que el JS lo pueda usar
        self.fields['categoria'].widget.attrs['data-submap'] = json.dumps(Producto.SUBCATEGORIAS)


class AdministrarProducto(admin.ModelAdmin):
    form = ProductoAdminForm
    readonly_fields = ('created', 'updated')
    list_display = ('titulo', 'precio', 'categoria', 'tamaño', 'color', 'ubicacion', 'vendedor', 'created')
    list_editable = ('precio', 'categoria', 'tamaño', 'color', 'ubicacion')
    search_fields = ('titulo', 'descripcion', 'categoria', 'ubicacion', 'vendedor__username')
    date_hierarchy = 'created'
    list_filter = ('categoria', 'tamaño', 'color', 'ubicacion', 'created', 'vendedor')
    ordering = ('-created',)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Si es superusuario, ve todo. Si es staff no super, limitamos a sus productos.
        if request.user.is_superuser:
            return qs
        # Usuarios staff no super solo ven sus propios productos
        if request.user.is_staff:
            return qs.filter(vendedor=request.user)
        # Otros no deberían estar aquí; devolvemos vacío por seguridad
        return qs.none()

    def save_model(self, request, obj, form, change):
        # Forzar que el vendedor sea el usuario que crea/edita (si no es superuser)
        if not request.user.is_superuser:
            obj.vendedor = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if not request.user.is_staff:
            return False
        if obj is None:
            return True
        return obj.vendedor == request.user

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if not request.user.is_staff:
            return False
        if obj is None:
            return True
        return obj.vendedor == request.user

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if not request.user.is_staff:
            return False
        if obj is None:
            return True
        return obj.vendedor == request.user

    def has_add_permission(self, request):
        # Staff puede agregar; se asigna automáticamente como vendedor
        return request.user.is_superuser or request.user.is_staff

    def get_readonly_fields(self, request, obj=None):
        # Evitar que staff cambie el vendedor manualmente
        ro = list(self.readonly_fields)
        if not request.user.is_superuser:
            ro.append('vendedor')
        return ro


admin.site.register(Producto, AdministrarProducto)
