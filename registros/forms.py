from django import forms
from django.forms import ModelForm, ClearableFileInput
from ckeditor.widgets import CKEditorWidget

from .models import ComentarioContacto, Archivos


class ComentarioContactoForm(forms.ModelForm):
    """
    Formulario para que los usuarios comunes creen comentarios de contacto.
    No requiere selección de alumno.
    """

    comentario = forms.CharField(widget=CKEditorWidget(), label="Comentario")

    class Meta:
        model = ComentarioContacto
        fields = ["usuario", "comentario"]
        labels = {
            "usuario": "Usuario",
            "comentario": "Comentario",
        }
        widgets = {
            "usuario": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingresa tu nombre"}
            ),
        }


class CustomClearableFileInput(ClearableFileInput):
    """
    Widget personalizado para mostrar el checkbox de borrar archivo y
    el input de reemplazo, como indica la actividad.
    """

    template_with_clear = (
        '<br><label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> '
        "%(clear)s"
    )


class FormArchivos(ModelForm):
    class Meta:
        model = Archivos
        fields = ("titulo", "descripcion", "archivo")
        widgets = {
            "archivo": CustomClearableFileInput,
        }
