from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from productos.models import Producto
from .models import PerfilUsuario
from .forms import PerfilUsuarioForm, RegistroForm, UserLoginForm


def login_view(request):
    """
    Vista de inicio de sesión usando UserLoginForm (basado en AuthenticationForm).
    """
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('home')
            messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('home')


def registro(request):
    """
    Vista de registro que crea tanto el usuario como su PerfilUsuario.
    """
    if request.method == 'POST':
        user_form = RegistroForm(request.POST)
        perfil_form = PerfilUsuarioForm(request.POST, request.FILES)
        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save()
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a SecondChance.')
            return redirect('home')
        messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        user_form = RegistroForm()
        perfil_form = PerfilUsuarioForm()

    return render(
        request,
        'registro.html',
        {
            'user_form': user_form,
            'perfil_form': perfil_form,
        },
    )


@login_required
def perfil(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)
    productos = Producto.objects.filter(vendedor=request.user) if perfil.tipo_usuario == 'vendedor' else []
    resenas = request.user.resenas_dadas.all()
    return render(
        request,
        'perfil.html',
        {
            'perfil': perfil,
            'productos': productos,
            'resenas': resenas,
        },
    )


@login_required
def editar_perfil(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('usuarios:perfil')
    else:
        form = PerfilUsuarioForm(instance=perfil)
    return render(request, 'editar_perfil.html', {'form': form})
