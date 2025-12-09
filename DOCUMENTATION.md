<style>
/* Estilos sencillos para mejorar lectura en renderizadores que acepten HTML */
body { font-family: "Inter", "Segoe UI", system-ui, sans-serif; line-height: 1.6; color: #1f2933; background: #f8fafc; }
h1, h2, h3, h4 { color: #0f172a; margin-top: 1.2em; }
code, pre { background: #0f172a; color: #e2e8f0; border-radius: 6px; padding: 0.2em 0.35em; }
pre { padding: 1em; overflow: auto; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #cbd5e1; padding: 8px; text-align: left; }
blockquote { border-left: 4px solid #38bdf8; padding-left: 1em; color: #0f172a; background: #e0f2fe; }
a { color: #0ea5e9; text-decoration: none; }
a:hover { text-decoration: underline; }
</style>

<!--
Si el renderizador no aplica CSS embebido, enlaza un docs.css:
<link rel="stylesheet" href="docs.css">
-->

# DOCUMENTATION.md

## Metadatos
- **Proyecto:** SecondChance (Marketplace Django)
- **Descripción:** Plataforma de compraventa de productos de segunda mano con categorías, subcategorías, filtros, reseñas y admin personalizado.
- **Autor:** Equipo SecondChance
- **Fecha:** 2025-12-06
- **Versión:** 1.0.0
- **Badges:**  
  - Build: ![build](https://placeholder/build.svg)  
  - Coverage: ![coverage](https://placeholder/coverage.svg)  
  - Python: ![python](https://placeholder/python.svg)  
  - Django: ![django](https://placeholder/django.svg)

## Tabla de contenidos
1. [Introducción](#introducción)  
   1.1 [Objetivo](#objetivo)  
   1.2 [Público objetivo](#público-objetivo)  
   1.3 [Requisitos previos](#requisitos-previos)
2. [Diseño y estilos (PARTE 1)](#diseño-y-estilos-parte-1)  
   2.1 [Estructura de templates](#estructura-de-templates)  
   2.2 [Sistema de assets (static)](#sistema-de-assets-static)  
   2.3 [CSS / frameworks sugeridos](#css--frameworks-sugeridos)  
   2.4 [Imágenes y media](#imágenes-y-media)  
   2.5 [Accesibilidad y responsive](#accesibilidad-y-responsive)  
   2.6 [Estilos en el .md](#estilos-en-el-md)
3. [Funciones, usos y admin (PARTE 2)](#funciones-usos-y-características-del-manejo-del-admin-parte-2)  
   3.1 [¿Qué gestiona el admin?](#qué-gestiona-el-admin)  
   3.2 [Personalización](#personalización-del-admin)  
   3.3 [Inlines y relaciones](#inlines-y-relaciones)  
   3.4 [Acciones personalizadas](#acciones-personalizadas)  
   3.5 [Permisos y grupos](#permisos-y-grupos)  
   3.6 [UI/UX admin](#uiux-del-admin)  
   3.7 [Automatizaciones](#automatizaciones-desde-admin)  
   3.8 [Export/Import](#exportimport-desde-admin)
4. [Funcionalidades extras avanzadas (PARTE 3)](#funcionalidades-extras-avanzadas-parte-3)  
   4.1 [Autenticación y autorización](#autenticación-y-autorización)  
   4.2 [Vistas y manejo de objetos](#vistas-y-manejo-de-objetos)  
   4.3 [Filtros y búsquedas](#filtros-y-búsquedas)  
   4.4 [Paginación](#paginación)  
   4.5 [API y serialización](#api-y-serialización)  
   4.6 [AJAX / JS](#llamado-de-objetos-desde-js--ajax)  
   4.7 [Subidas y validación](#subidas-de-archivos-y-validación)  
   4.8 [Caching y performance](#caching-y-performance)  
   4.9 [Tareas asíncronas](#tareas-asíncronas)  
   4.10 [Websockets](#websockets--tiempo-real-opcional)  
   4.11 [Tests](#tests-automatizados)  
   4.12 [Logging](#logging-y-monitoreo)  
   4.13 [Mejores prácticas](#mejores-prácticas-de-código)
5. [Ejemplos de código](#ejemplos-de-código)
6. [Comandos rápidos](#comandos-rápidos)
7. [Arquitectura y estructura de archivos](#arquitectura-y-estructura-de-archivos)
8. [Seguridad y configuración para producción](#seguridad-y-configuración-para-producción)
9. [Despliegue](#despliegue)
10. [Testing y CI](#testing-y-ci)
11. [Mantenimiento y operaciones](#mantenimiento-y-operaciones)
12. [FAQ / Troubleshooting](#faq--troubleshooting)
13. [Checklist de documentación](#checklist-de-documentación)
14. [Notas rápidas](#notas-rápidas)
15. [Cómo contribuir](#cómo-contribuir)
16. [Changelog](#changelog)
17. [Archivos relacionados](#archivos-relacionados)
18. [Referencias](#referencias)

---

## Introducción
### Objetivo
Documentar de forma clara la estructura, estilos, administración y funcionalidades avanzadas de la aplicación Django “SecondChance”, sirviendo como guía de desarrollo, mantenimiento y despliegue.

### Público objetivo
Desarrolladores Django de nivel intermedio, DevOps responsables de despliegue y QA/analistas que validan funcionalidades.

### Requisitos previos
- Python 3.10+  
- pip y virtualenv  
- Base de datos: PostgreSQL (recomendado) o SQLite para desarrollo  
- Git, Node/NPM (opcional si se usa Tailwind/Vite)

---

## Diseño y estilos (PARTE 1)
### Estructura de templates
- Uso de `base.html` con bloques `{% block title %}` y `{% block content %}`.
- Herencia en templates de secciones (`home.html`, `catalogo.html`, etc.).
- Ejemplo `base.html` (fragmento):
```html
{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}SecondChance{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
  <nav>... navbar ...</nav>
  <main class="container">
    {% block content %}{% endblock %}
  </main>
</body>
</html>
```
- Ejemplo `home.html`:
```html
{% extends 'base.html' %}
{% block title %}Inicio - SecondChance{% endblock %}
{% block content %}
<section class="hero">
  <h1>SecondChance</h1>
  <p>Encuentra y vende productos de segunda mano.</p>
</section>
{% endblock %}
```

### Sistema de assets (static)
- Ubicación típica: `app/static/app/...` y `STATICFILES_DIRS` para assets globales.
- Comando `python manage.py collectstatic` recopila en `STATIC_ROOT`.
- Organización sugerida:
  ```
  static/
    css/
    js/
    images/
  ```

### CSS / frameworks sugeridos
- Puedes usar Bootstrap/Tailwind o CSS propio.
- Ejemplo de import de Bootstrap en `base.html`:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
```
- Tailwind (opcional): instalar con npm, configurar `tailwind.config.js`, y generar el CSS.

### Imágenes y media
- Configurar en `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```
- Ejemplo de modelo con `ImageField`:
```python
class Producto(models.Model):
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)
```
- En template:
```html
{% if producto.imagen %}
  <img src="{{ producto.imagen.url }}" alt="{{ producto.titulo }}">
{% endif %}
```
- Recomendación: instalar Pillow.

### Accesibilidad y responsive
- Incluir `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.
- Usar contrastes adecuados, labels asociadas a inputs, `aria-label` en iconos.

### Estilos en el .md
- El bloque `<style>` al inicio mejora legibilidad; si el renderizador no soporta, enlazar `docs.css`.

---

## Funciones, usos y características del manejo del admin (PARTE 2)
### ¿Qué gestiona el admin?
- Modelos clave: `Producto`, `PerfilUsuario`, `Resena`.
- Permite CRUD de productos, reseñas, perfiles y gestión de vendedores.

### Personalización del admin
- Ajustes comunes: `list_display`, `list_filter`, `search_fields`, `ordering`, `list_editable`.
- Ejemplo `admin.py` (simplificado):
```python
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio', 'categoria', 'subcategoria', 'vendedor', 'created')
    list_filter = ('categoria', 'subcategoria', 'created')
    search_fields = ('titulo', 'descripcion')
    ordering = ('-created',)
    list_editable = ('precio', 'categoria', 'subcategoria')
```

### Inlines y relaciones
- Ejemplo TabularInline para reseñas:
```python
class ResenaInline(admin.TabularInline):
    model = Resena
    extra = 0
```

### Acciones personalizadas
- Acción masiva para marcar como publicado:
```python
def marcar_publicado(modeladmin, request, queryset):
    queryset.update(publicado=True)
```
- Agregar en `actions = [marcar_publicado]`.

### Permisos y grupos
- Filtrar queryset por usuario (vendedores):
```python
def get_queryset(self, request):
    qs = super().get_queryset(request)
    return qs if request.user.is_superuser else qs.filter(vendedor=request.user)
```

### UI/UX del admin
- `fieldsets`, `readonly_fields`, `prepopulated_fields` para mejorar edición.
- `list_per_page` para paginar.

### Automatizaciones desde admin
- Hooks: `save_model`, `delete_model`; señales para logging o actualizaciones.

### Export/Import desde admin
- Recomendación: paquete `django-import-export` para CSV/XLSX.

---

## Funcionalidades extras avanzadas (PARTE 3)
### Autenticación y autorización
- Uso de `django.contrib.auth`.
- Ejemplo `urls.py` para login/logout:
```python
from django.contrib.auth import views as auth_views
urlpatterns = [
  path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
```
- Decoradores: `@login_required`, mixins `PermissionRequiredMixin`.

### Vistas y manejo de objetos
- CBV: `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`.
- FBV: uso de `get_object_or_404`.
- Optimización: `select_related`, `prefetch_related`.

### Filtros y búsquedas
- `django-filter`: `pip install django-filter`.
- Ejemplo simple:
```python
import django_filters
class ProductoFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Producto
        fields = ['categoria', 'subcategoria']
```
- Búsqueda con `__icontains`; para Postgres, `TrigramSimilarity` en búsquedas avanzadas.

### Paginación
- Con `Paginator` o `ListView(paginate_by=...)`.

### API y serialización
- DRF: `pip install djangorestframework`.
- Serializer:
```python
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
```
- ViewSet + router:
```python
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
```

### Llamado de objetos desde JS / AJAX
- Uso de `fetch` a un endpoint JSON de sugerencias:
```js
fetch('/catalogo/suggest/?q=camisa').then(r=>r.json());
```

### Subidas de archivos y validación
- Validar tamaño/tipo en `clean()` o en el form.
- Almacenamiento seguro; usar backends (S3) en producción.

### Caching y performance
- Configurar cache en `settings.py` (filebased/redis).
- `@cache_page` y fragment caching para bloques.

### Tareas asíncronas
- Celery: `pip install celery`.
- Tarea simple:
```python
@app.task
def enviar_resumen():
    ...
```

### Websockets / tiempo real (opcional)
- Django Channels para chat/notificaciones.

### Tests automatizados
- `TestCase` para modelos, vistas y formularios.
- Ejemplo:
```python
class ProductoModelTest(TestCase):
    def test_str(self):
        p = Producto(titulo="X")
        self.assertEqual(str(p), "X")
```

### Logging y monitoreo
- Configurar `LOGGING` en settings.
- Recomendación: Sentry/Papertrail.

### Mejores prácticas de código
- PEP8, `flake8`, `black`, hints con `mypy`.

---

## Ejemplos de código
### Modelo Product completo
```python
class Producto(models.Model):
    CATEGORIA_CHOICES = [('ropa','Ropa'), ('electronicos','Electrónicos')]
    SUBCATEGORIAS = {
        'ropa': [('camisas','Camisas y playeras')],
        'electronicos': [('smartphones','Smartphones')],
    }
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    subcategoria = models.CharField(max_length=50, blank=True, choices=[
        (clave,label) for cat, subs in SUBCATEGORIAS.items() for clave,label in subs
    ])
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']
    def __str__(self):
        return self.titulo
```

### admin.py con filtros y acción
```python
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo','precio','categoria','subcategoria','vendedor','created')
    list_filter = ('categoria','subcategoria','created')
    search_fields = ('titulo','descripcion')
    actions = ['marcar_publicado']

    def marcar_publicado(self, request, queryset):
        queryset.update(publicado=True)
```

### views.py CBV paginada y optimizada
```python
class CatalogoView(ListView):
    model = Producto
    template_name = 'catalogo.html'
    paginate_by = 12

    def get_queryset(self):
        qs = Producto.objects.all().select_related('vendedor')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(titulo__icontains=q) | Q(descripcion__icontains=q))
        return qs
```

### urls.py
```python
urlpatterns = [
  path('', CatalogoView.as_view(), name='catalogo'),
  path('<int:pk>/', DetalleProductoView.as_view(), name='detalle_producto'),
]
```

### Template lista con paginación
```html
{% for p in object_list %}
  <div>{{ p.titulo }} - ${{ p.precio }}</div>
{% endfor %}
{% if is_paginated %}
  {% if page_obj.has_previous %}<a href="?page={{ page_obj.previous_page_number }}">Anterior</a>{% endif %}
  Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}
  {% if page_obj.has_next %}<a href="?page={{ page_obj.next_page_number }}">Siguiente</a>{% endif %}
{% endif %}
```

### DRF endpoint
```python
from rest_framework import viewsets, serializers

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
```

### forms.py validación personalizada
```python
class ProductoForm(forms.ModelForm):
    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio <= 0:
            raise forms.ValidationError("Precio debe ser mayor a 0")
        return precio
```

### tests básicos
```python
class ProductoViewTest(TestCase):
    def test_list_status(self):
        resp = self.client.get('/catalogo/')
        self.assertEqual(resp.status_code, 200)
```

---

## Comandos rápidos
```bash
# Crear entorno
python -m venv .venv
source .venv/bin/activate  # win: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate

# Superusuario
python manage.py createsuperuser

# Runserver
python manage.py runserver

# Static
python manage.py collectstatic
```

---

## Arquitectura y estructura de archivos
```
project/
  manage.py
  project/            # settings, urls, wsgi/asgi
  apps/
    productos/        # models, views, urls, forms, admin
    usuarios/
  templates/          # base, catalogo, login, etc.
  static/             # css, js, images
  media/              # uploads (ImageField)
  requirements.txt
  .env
  Procfile
  Dockerfile
```
- `project/settings.py`: configuración global.
- `apps/*`: lógica de negocio.
- `templates/`: HTML con herencia.
- `static/`: assets.
- `media/`: archivos subidos.
- `.env`: variables sensibles (SECRET_KEY, DB).
- `Dockerfile/Procfile`: despliegue.

---

## Seguridad y configuración para producción
- `DEBUG=False`, `SECRET_KEY` en env.
- `ALLOWED_HOSTS` configurado.
- HTTPS, HSTS, CSRF seguro, SESSION_COOKIE_SECURE.
- CSP y cabeceras de seguridad (via middleware/NGINX).
- Validar uploads (tamaño/tipo).
- Rotar logs y backups.

---

## Despliegue
- Gunicorn + Nginx: servir Django + static via Nginx.
- Variables de entorno (SECRET_KEY, DB, ALLOWED_HOSTS).
- `collectstatic`, `migrate` en release.
- Docker: gunicorn en el contenedor; Nginx reverse proxy.

---

## Testing y CI
- Pipeline básico (GitHub Actions):
```yaml
- uses: actions/checkout@v3
- uses: actions/setup-python@v4
  with: { python-version: '3.10' }
- run: pip install -r requirements.txt
- run: python manage.py test
```
- Añadir `flake8/black` y `coverage` según necesidad.

---

## Mantenimiento y operaciones
- Backups de DB regulares.
- Rotación de logs.
- Monitoreo (Sentry, health checks).
- Actualizar dependencias con cuidado (`pip-compile`/`poetry`).

---

## FAQ / Troubleshooting
- Migraciones no aplican: borrar migraciones rotas, recrear, `migrate --fake` con precaución.
- Static en producción: revisar `STATIC_ROOT`, permisos, Nginx.
- Errores de admin: revisar permisos y `get_queryset`.
- CORS: configurar `django-cors-headers` si expones API.

---

## Checklist de documentación
- [ ] README y este DOCUMENTATION.md actualizados.
- [ ] Variables en `.env` documentadas.
- [ ] Scripts de setup y despliegue probados.
- [ ] Tests básicos pasando.
- [ ] Instrucciones de backup y restore anotadas.

---

## Notas rápidas
- Usa `select_related`/`prefetch_related` en listas.
- Limita `list_editable` a pocos campos en admin.
- No expongas SECRET_KEY ni DEBUG en prod.
- Revisa logs y métricas tras cada despliegue.
- Usa `login_required` en vistas sensibles.

---

## Cómo contribuir
1. Haz fork y crea rama `feature/tu-feature`.
2. Ejecuta tests antes de PR.
3. Sigue PEP8; formatea con `black`.
4. Abre PR con descripción y capturas si aplica.

---

## Changelog
- **1.0.0 (2025-12-06):** Documentación inicial, guía de admin, filtros, auth, despliegue y ejemplos de código.

---

## Archivos relacionados
- `apps/productos/models.py`
- `apps/productos/admin.py`
- `apps/productos/forms.py`
- `apps/productos/views.py`, `apps/productos/urls.py`
- `templates/base.html`, `templates/catalogo.html`
- `static/css/style.css`
- `project/settings.py`

---

## Referencias
- Django docs (buscar: “Django documentation”)
- Django admin docs (buscar: “Django admin site”)
- django-filter (buscar: “django-filter readthedocs”)
- django-allauth (buscar: “django-allauth docs”)
- Django REST Framework (buscar: “DRF documentation”)






