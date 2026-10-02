from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Bienvenido a GrowUp, {user.username}! Tu cuenta ha sido creada exitosamente.")
            return redirect('catalog:home')
        else:
            messages.error(request, "Por favor corrige los errores señalados a continuación.")
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"¡Bienvenido de vuelta, {user.username}!")
            next_url = request.GET.get('next') or 'catalog:home'
            return redirect(next_url)
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('catalog:home')


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.email = form.cleaned_data.get('email', '')
            user.save()
            form.save()
            messages.success(request, "Tu perfil ha sido actualizado correctamente.")
            return redirect('accounts:profile')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = ProfileUpdateForm(instance=profile, initial=initial)

    user_reviews = request.user.reviews.all().order_by('-created_at')[:10]
    user_novels = request.user.novels.all().order_by('-created_at') if profile.is_author else []

    context = {
        'form': form,
        'profile': profile,
        'user_reviews': user_reviews,
        'user_novels': user_novels,
    }
    return render(request, 'accounts/profile.html', context)
