from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('subir/', views.subir_producto, name='subir_producto'),
    path('<int:producto_id>/editar/', views.editar_producto, name='editar_producto'),
    path('<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('suggest/', views.producto_suggest, name='producto_suggest'),
]
