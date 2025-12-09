from django.shortcuts import render
from productos.models import Producto

def home(request):
    productos_destacados = Producto.objects.all()[:6]  # 6 productos destacados
    return render(request, 'home.html', {'productos_destacados': productos_destacados})

def sobre_nosotros(request):
    return render(request, 'sobre_nosotros.html')

def contacto(request):
    if request.method == 'POST':
        # Aquí iría la lógica para enviar el email o guardar el mensaje
        pass
    return render(request, 'contacto.html')
