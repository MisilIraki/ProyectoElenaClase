from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Producto(models.Model):
    SUBCATEGORIAS = {
        'ropa': [
            ('camisas', 'Camisas y playeras'),
            ('calzado', 'Calzado'),
            ('accesorios', 'Accesorios'),
        ],
        'electronicos': [
            ('smartphones', 'Smartphones'),
            ('accesorios', 'Accesorios'),
            ('gadgets', 'Tablets / Gadgets'),
        ],
        'muebles': [
            ('decoracion', 'Decoración'),
            ('textiles', 'Textiles y tapetes'),
            ('cocina', 'Cocina y comedor'),
        ],
        'libros': [
            ('ficcion', 'Ficción'),
            ('academico', 'Académico'),
            ('infantil', 'Infantil / Jóvenes'),
        ],
        'accesorios': [
            ('bolsas', 'Bolsas'),
            ('joyeria', 'Lentes / Joyas'),
            ('carteras', 'Carteras / Billeteras'),
        ],
        'otros': [
            ('coleccion', 'Coleccionables'),
            ('retro', 'Retro / Vintage'),
            ('rareza', 'Rarezas'),
        ],
    }

    TAMAÑO_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]

    COLOR_CHOICES = [
        ('azul', 'Azul'),
        ('rojo', 'Rojo'),
        ('verde', 'Verde'),
        ('negro', 'Negro'),
        ('blanco', 'Blanco'),
        ('amarillo', 'Amarillo'),
        ('rosa', 'Rosa'),
        ('morado', 'Morado'),
        ('naranja', 'Naranja'),
        ('gris', 'Gris'),
        ('marrón', 'Marrón'),
        ('turquesa', 'Turquesa'),
    ]

    CATEGORIA_CHOICES = [
        ('ropa', 'Ropa'),
        ('electronicos', 'Electrónicos'),
        ('muebles', 'Muebles'),
        ('libros', 'Libros'),
        ('accesorios', 'Accesorios'),
        ('otros', 'Otros'),
    ]

    SUBCATEGORIA_CHOICES = [
        (clave, label) for cat, subs in SUBCATEGORIAS.items() for clave, label in subs
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título", help_text="Ej: Camisa de algodón talla M")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio",
        validators=[MinValueValidator(0.01)],
        help_text="Introduce el precio en MXN, mayor que 0.",
    )
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIA_CHOICES,
        verbose_name="Categoría",
        help_text="Selecciona la categoría que mejor describe el producto.",
    )
    subcategoria = models.CharField(
        max_length=50,
        choices=SUBCATEGORIA_CHOICES,
        blank=True,
        verbose_name="Subcategoría",
        help_text="Subcategoría asociada a la categoría elegida.",
    )
    tamaño = models.CharField(max_length=2, choices=TAMAÑO_CHOICES, blank=True, verbose_name="Tamaño")
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, blank=True, verbose_name="Color")
    ubicacion = models.CharField(max_length=100, verbose_name="Ubicación")
    imagen = models.ImageField(upload_to="productos", null=True, blank=True, verbose_name="Imagen")
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Vendedor")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["-created"]

    def __str__(self):
        return self.titulo
