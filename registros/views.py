from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages

from .models import Alumnos, ComentarioContacto, Archivos
from .forms import ComentarioContactoForm, FormArchivos

def registros_inicio(request):
    """Vista principal que muestra todos los alumnos"""
    alumnos = Alumnos.objects.all()
    return render(request, 'inicio/principal.html', {'alumnos': alumnos})

def consultarComentario(request):
    """Vista para consultar todos los comentarios de contacto."""
    comentarios = ComentarioContacto.objects.all()
    return render(request, 'registros/consultar_comentarios.html', {'comentarios': comentarios})

def editarComentarioContacto(request, id):
    """Editar un comentario de contacto existente."""
    comentario = get_object_or_404(ComentarioContacto, id=id)

    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('ConsultarComentario')
    else:
        form = ComentarioContactoForm(instance=comentario)

    return render(request, 'registros/editar_comentario_contacto.html', {
        'form': form,
        'comentario': comentario
    })

def eliminarComentario(request, id):
    """Eliminar un comentario de contacto, mostrando confirmación."""
    confirmacion = 'registros/eliminar_alumno.html'
    comentario = get_object_or_404(ComentarioContacto, id=id)

    if request.method == 'POST':
        comentario.delete()
        return redirect('ConsultarComentario')

    return render(request, confirmacion, {'comentario': comentario})

def _render_alumnos_consulta(request, queryset, titulo, descripcion=None):
    """Renderiza la plantilla de consultas con un queryset de alumnos."""
    contexto = {
        'titulo': titulo,
        'descripcion': descripcion,
        'alumnos': queryset
    }
    return render(request, 'registros/consultas.html', contexto)

def _render_contacto_consulta(request, comentarios, titulo, descripcion=None, solo_comentarios_texto=False):
    """Renderiza consultas de comentarios de contacto."""
    contexto = {
        'titulo': titulo,
        'descripcion': descripcion,
        'comentarios': comentarios,
        'solo_texto': solo_comentarios_texto
    }
    return render(request, 'registros/consultas_contacto.html', contexto)

def consultar1(request):
    """Consulta con una sola condición (carrera TI)."""
    alumnos = Alumnos.objects.filter(carrera="TI")
    return _render_alumnos_consulta(
        request,
        alumnos,
        "Consulta 1: carrera TI",
        "Retorna a los alumnos que estudian en la carrera TI."
    )

def consultar2(request):
    """Consulta con múltiples condiciones (carrera y turno)."""
    alumnos = Alumnos.objects.filter(carrera="TI", turno="Matutino")
    return _render_alumnos_consulta(
        request,
        alumnos,
        "Consulta 2: TI Matutino",
        "Alumnos de TI que además cursan turno matutino."
    )

def consultar3(request):
    """Recupera solo los campos necesarios con .only()."""
    alumnos = Alumnos.objects.all().only("matricula", "nombre", "carrera", "turno", "imagen")
    return _render_alumnos_consulta(
        request,
        alumnos,
        "Consulta 3: solo campos principales",
        "Utiliza .only() para solicitar únicamente los campos solicitados por el PDF."
    )

def consultar4(request):
    """Busca con expresiones sobre el turno."""
    alumnos = Alumnos.objects.filter(turno__contains="Vesp")
    return _render_alumnos_consulta(
        request,
        alumnos,
        "Consulta 4: turno contiene Vesp",
        "Filtro que aprovecha el lookup __contains."
    )

def consultar5(request):
    """Consulta con expresiones __in."""
    alumnos = Alumnos.objects.filter(nombre__in=["Juan", "Ana"])
    return _render_alumnos_consulta(
        request,
        alumnos,
        "Consulta 5: nombres Juan o Ana",
        "Lookup __in para buscar alumnos específicos."
    )

def consultar6(request):
    """Consulta por rango de fechas."""
    fecha_inicio = date(2022, 7, 1)
    fecha_fin = date(2022, 7, 13)
    alumnos = Alumnos.objects.filter(created__date__range=(fecha_inicio, fecha_fin))
    return _render_alumnos_consulta(
        request,
        alumnos,
        "Consulta 6: rango de creación",
        "Busca alumnos registrados entre el 1 y 13 de julio de 2022."
    )

def consultar7(request):
    """Consulta entre modelos usando el comentario relacionado."""
    alumnos = Alumnos.objects.filter(comentario__coment__contains='No Inscrito')
    return _render_alumnos_consulta(
        request,
        alumnos,
        "Consulta 7: alumnos con comentario que contiene 'No Inscrito'",
        "Relaciona el modelo Comentario para encontrar coincidencias."
    )

def consultar_contacto_fecha(request):
    """Consulta comentarios entre dos fechas entregadas en la hoja de actividades."""
    rango_inicio = date(2025, 11, 20)
    rango_fin = date(2025, 11, 26)
    comentarios = ComentarioContacto.objects.filter(created__date__range=(rango_inicio, rango_fin))
    return _render_contacto_consulta(
        request,
        comentarios,
        "Actividad: comentarios entre 20 y 26 de noviembre",
        "Filtra utilizando el rango solicitado para los comentarios de contacto."
    )

def consultar_contacto_expresion(request):
    """Consulta por texto dentro del comentario usando __icontains."""
    comentarios = ComentarioContacto.objects.filter(comentario__icontains='inscrito')
    return _render_contacto_consulta(
        request,
        comentarios,
        "Actividad: búsqueda textual",
        "Uso de __icontains para encontrar la palabra 'inscrito'."
    )

def consultar_contacto_usuario(request):
    """Consulta comentarios por usuario."""
    usuario = request.GET.get('usuario', 'Administrador')
    comentarios = ComentarioContacto.objects.filter(usuario__iexact=usuario)
    return _render_contacto_consulta(
        request,
        comentarios,
        f"Actividad: comentarios del usuario {usuario}",
        "Ejemplo de filtro exacto (sin distinción de mayúsculas)."
    )

def consultar_contacto_solo_comentarios(request):
    """Retorna únicamente el texto de los comentarios."""
    comentarios_texto = list(ComentarioContacto.objects.values_list('comentario', flat=True))
    return _render_contacto_consulta(
        request,
        comentarios_texto,
        "Actividad: solo comentarios",
        "Esta vista muestra únicamente el texto de cada comentario.",
        solo_comentarios_texto=True
    )

def consultar_contacto_exp_diferente(request):
    """Utiliza un lookup distinto (startswith) sobre la columna usuario."""
    comentarios = ComentarioContacto.objects.filter(usuario__startswith='A')
    return _render_contacto_consulta(
        request,
        comentarios,
        "Actividad: nueva expresión",
        "Lookup __startswith como nueva expresión (distinta a __contains o __range).",
    )


def archivos(request):
    """
    Vista para carga de archivos según la actividad.
    """

    if request.method == "POST":
        form = FormArchivos(request.POST, request.FILES)
        if form.is_valid():
            # Podemos usar directamente form.save(), pero seguimos la guía.
            titulo = request.POST["titulo"]
            descripcion = request.POST.get("descripcion", "")
            archivo = request.FILES.get("archivo")

            Archivos.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                archivo=archivo,
            )
            messages.success(request, "Archivo cargado correctamente.")
            return render(request, "registros/archivos.html")
        else:
            messages.error(request, "Error al procesar el formulario")
    # GET o POST inválido: mostrar formulario vacío
    form = FormArchivos()
    return render(
        request,
        "registros/archivos.html",
        {"form": form, "archivos": Archivos.objects.all()},
    )
