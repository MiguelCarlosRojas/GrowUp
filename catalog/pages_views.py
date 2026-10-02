from django.shortcuts import render
from django.contrib import messages

def quienes_somos_view(request):
    return render(request, 'pages/quienes_somos.html')

def nuestra_historia_view(request):
    return render(request, 'pages/nuestra_historia.html')

def donde_estamos_view(request):
    return render(request, 'pages/donde_estamos.html')

def blog_view(request):
    return render(request, 'pages/blog.html')

def ayuda_view(request):
    return render(request, 'pages/ayuda.html')

def preguntas_frecuentes_view(request):
    return render(request, 'pages/preguntas_frecuentes.html')

def contacto_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        asunto = request.POST.get('asunto', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()
        if nombre and email and mensaje:
            messages.success(request, f"¡Gracias por comunicarte con nosotros, {nombre}! Tu mensaje ha sido recibido por nuestro equipo de soporte.")
        else:
            messages.error(request, "Por favor completa todos los campos requeridos del formulario.")
    return render(request, 'pages/contacto.html')

def aviso_legal_view(request):
    return render(request, 'pages/aviso_legal.html')

def politica_cookies_view(request):
    return render(request, 'pages/politica_cookies.html')

def condiciones_uso_view(request):
    return render(request, 'pages/condiciones_uso.html')

def politica_privacidad_view(request):
    return render(request, 'pages/politica_privacidad.html')

def declaracion_accesibilidad_view(request):
    return render(request, 'pages/declaracion_accesibilidad.html')
