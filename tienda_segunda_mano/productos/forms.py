from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['titulo', 'descripcion', 'precio', 'categoria', 'subcategoria', 'tamaño', 'color', 'ubicacion', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-select', 'id': 'id_categoria'}),
            'subcategoria': forms.Select(attrs={'class': 'form-select', 'id': 'id_subcategoria'}),
            'tamaño': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.Select(attrs={'class': 'form-select'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajusta subcategorías según la categoría seleccionada
        categoria = None
        if self.data.get('categoria'):
            categoria = self.data.get('categoria')
        elif self.instance and self.instance.pk:
            categoria = self.instance.categoria
        subs = Producto.SUBCATEGORIAS.get(categoria, [])
        self.fields['subcategoria'].choices = [('', '---------')] + subs

    def clean(self):
        cleaned = super().clean()
        categoria = cleaned.get('categoria')
        subcategoria = cleaned.get('subcategoria')
        if subcategoria:
            valid_subs = dict(Producto.SUBCATEGORIAS.get(categoria, []))
            if subcategoria not in valid_subs:
                self.add_error('subcategoria', 'La subcategoría no coincide con la categoría seleccionada.')
        return cleaned
