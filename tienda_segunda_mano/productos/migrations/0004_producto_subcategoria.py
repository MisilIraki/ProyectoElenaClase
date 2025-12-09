from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_alter_producto_categoria_alter_producto_precio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='subcategoria',
            field=models.CharField(blank=True, choices=[('camisas', 'Camisas y playeras'), ('calzado', 'Calzado'), ('accesorios', 'Accesorios'), ('smartphones', 'Smartphones'), ('accesorios', 'Accesorios'), ('gadgets', 'Tablets / Gadgets'), ('decoracion', 'Decoración'), ('textiles', 'Textiles y tapetes'), ('cocina', 'Cocina y comedor'), ('ficcion', 'Ficción'), ('academico', 'Académico'), ('infantil', 'Infantil / Jóvenes'), ('bolsas', 'Bolsas'), ('joyeria', 'Lentes / Joyas'), ('carteras', 'Carteras / Billeteras'), ('coleccion', 'Coleccionables'), ('retro', 'Retro / Vintage'), ('rareza', 'Rarezas')], help_text='Subcategoría asociada a la categoría elegida.', max_length=50, verbose_name='Subcategoría'),
        ),
    ]






