from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from decimal import Decimal
import re
import urllib.parse
from django.http import JsonResponse
from .models import Producto
from .forms import ProductoForm
from usuarios.forms import ResenaForm
from usuarios.models import Resena, PerfilUsuario

def catalogo(request):
    productos = Producto.objects.all()
    query = request.GET.get('q')
    categoria = request.GET.get('categoria')
    tamaño = request.GET.get('tamaño')
    colors = request.GET.getlist('color')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')

    if query:
        productos = productos.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query))
    if categoria:
        # Usamos iexact para tolerar mayúsculas/minúsculas heredadas
        productos = productos.filter(categoria__iexact=categoria)
    if tamaño:
        productos = productos.filter(tamaño=tamaño)
    if colors:
        productos = productos.filter(color__in=colors)
    if precio_min:
        try:
            min_price = Decimal(precio_min)
            productos = productos.filter(precio__gte=min_price)
        except ValueError:
            pass
    if precio_max:
        try:
            max_price = Decimal(precio_max)
            productos = productos.filter(precio__lte=max_price)
        except ValueError:
            pass

    # Grid paginado estándar
    paginator = Paginator(productos, 12)  # 12 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Usamos las categorías oficiales del modelo para evitar duplicados
    categorias = Producto.CATEGORIA_CHOICES
    tamaños = Producto.objects.values_list('tamaño', flat=True).distinct().exclude(tamaño__isnull=True).exclude(tamaño__exact='')
    colores = Producto.objects.values_list('color', flat=True).distinct().exclude(color__isnull=True).exclude(color__exact='')

    # Segmentación inicial: si no hay filtros activos, mostrar bloques por categoría
    has_filters = any([query, categoria, tamaño, colors, precio_min, precio_max])
    secciones_categoria = []
    if not has_filters:
        for cat_val, cat_label in categorias:
            qs_cat = Producto.objects.filter(categoria__iexact=cat_val).order_by('-created')[:8]
            if qs_cat:
                secciones_categoria.append({
                    'slug': cat_val,
                    'label': cat_label,
                    'items': qs_cat,
                })

    return render(request, 'catalogo.html', {
        'productos': page_obj,
        'query': query,
        'categoria': categoria,
        'tamaño': tamaño,
        'colors': colors,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'categorias': categorias,
        'tamaños': tamaños,
        'colores': colores,
        'secciones_categoria': secciones_categoria,
        'has_filters': has_filters,
    })

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    resenas = Resena.objects.filter(producto=producto)
    avg_rating = resenas.aggregate(promedio=Avg('rating'))['promedio']

    # CTA de contacto dinámico (no se muestra por ahora; se deja preparado para futuro uso)
    vendedor_perfil, _ = PerfilUsuario.objects.get_or_create(user=producto.vendedor)
    telefono_raw = vendedor_perfil.telefono or ""
    telefono_digits = re.sub(r"\D", "", telefono_raw)
    whatsapp_url = None
    if telefono_digits:
        default_msg = f"Hola, vi tu producto '{producto.titulo}' en SecondChance y me interesa."
        whatsapp_url = f"https://wa.me/{telefono_digits}?text={urllib.parse.quote(default_msg)}"
    mailto_url = None
    if producto.vendedor.email:
        subject = f"Interés en tu producto: {producto.titulo}"
        body = f"Hola {producto.vendedor.username}, me interesa tu producto '{producto.titulo}'."
        mailto_url = f"mailto:{producto.vendedor.email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"

    # Manejo de reseña (crear/editar) por parte de usuarios autenticados
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Inicia sesión para dejar una reseña.')
            return redirect('usuarios:login')
        if producto.vendedor == request.user:
            messages.error(request, 'No puedes reseñarte a ti mismo.')
            return redirect('productos:detalle_producto', producto_id=producto.id)

        form = ResenaForm(request.POST)
        if form.is_valid():
            Resena.objects.update_or_create(
                reviewer=request.user,
                producto=producto,
                defaults={
                    'reviewed_user': producto.vendedor,
                    'comentario': form.cleaned_data['comentario'],
                    'rating': form.cleaned_data['rating'],
                }
            )
            messages.success(request, 'Tu reseña ha sido registrada.')
            return redirect('productos:detalle_producto', producto_id=producto.id)
    else:
        form = ResenaForm()

    return render(
        request,
        'detalle_producto.html',
        {
            'producto': producto,
            'resenas': resenas[:5],  # mostrar últimas 5 en el detalle
            'avg_rating': avg_rating,
            'resena_form': form,
        },
    )


def producto_suggest(request):
    """
    Endpoint de sugerencias de productos para autocompletado.
    Retorna JSON con id, titulo y url del detalle.
    """
    q = request.GET.get('q', '').strip()
    results = []
    if len(q) >= 2:
        qs = Producto.objects.filter(
            Q(titulo__icontains=q) | Q(descripcion__icontains=q)
        ).order_by('-created')[:8]
        results = [
            {
                'id': p.id,
                'titulo': p.titulo,
                'url': f"/catalogo/{p.id}/",
                'precio': str(p.precio),
            }
            for p in qs
        ]
    return JsonResponse({'results': results})

@login_required
def subir_producto(request):
    # Solo permiten subir productos los perfiles de tipo vendedor o superusuarios
    perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)
    if not (request.user.is_superuser or perfil.tipo_usuario == 'vendedor'):
        messages.error(request, 'Solo vendedores pueden subir productos.')
        return redirect('home')

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user
            producto.save()
            messages.success(request, 'Producto subido exitosamente.')
            return redirect('usuarios:perfil')
    else:
        form = ProductoForm()
    return render(request, 'subir_producto.html', {'form': form, 'subcats': Producto.SUBCATEGORIAS})

@login_required
def editar_producto(request, producto_id):
    if not request.user.is_superuser:
        messages.error(request, 'Solo administradores pueden editar productos.')
        return redirect('home')
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('usuarios:perfil')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'subir_producto.html', {'form': form, 'subcats': Producto.SUBCATEGORIAS})

@login_required
def eliminar_producto(request, producto_id):
    if not request.user.is_superuser:
        messages.error(request, 'Solo administradores pueden eliminar productos.')
        return redirect('home')
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('usuarios:perfil')
    return render(request, 'confirmar_eliminar.html', {'producto': producto})
