from django.db import migrations, models
import django.db.models.deletion


def fill_resena_producto(apps, schema_editor):
    Resena = apps.get_model('usuarios', 'Resena')
    Producto = apps.get_model('productos', 'Producto')

    to_delete = []
    for res in Resena.objects.filter(producto__isnull=True):
        producto = Producto.objects.filter(vendedor=res.reviewed_user).first()
        if producto:
            res.producto = producto
            res.save(update_fields=['producto'])
        else:
            # No hay producto asociado al vendedor; eliminamos la reseña huérfana
            to_delete.append(res.id)

    if to_delete:
        Resena.objects.filter(id__in=to_delete).delete()


def reverse_fill_resena_producto(apps, schema_editor):
    # Al revertir, simplemente dejamos producto en null para las reseñas afectadas
    Resena = apps.get_model('usuarios', 'Resena')
    Resena.objects.update(producto=None)


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_alter_producto_categoria_alter_producto_precio_and_more'),
        ('usuarios', '0003_resena_producto_resena_unique_reviewer_producto'),
    ]

    operations = [
        migrations.RunPython(fill_resena_producto, reverse_fill_resena_producto),
        migrations.AlterField(
            model_name='resena',
            name='producto',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='resenas',
                to='productos.producto',
                verbose_name='Producto'
            ),
        ),
    ]

