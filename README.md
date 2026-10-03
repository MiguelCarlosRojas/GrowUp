# GrowUp - Plataforma de Manga, Anime y Novelas Ligeras

[![Render Deployment](https://img.shields.io/badge/deployment-Render%20Live-22c55e.svg)](https://growup-7my7.onrender.com)
[![CI Compilation & Test Suite](https://github.com/MiguelCarlosRojas/GrowUp/actions/workflows/ci.yml/badge.svg)](https://github.com/MiguelCarlosRojas/GrowUp/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.1%2B%20%7C%206.1-green.svg)](https://www.djangoproject.com/)
[![Database](https://img.shields.io/badge/database-Prisma%20Postgres-3963F7.svg)](https://www.prisma.io/postgres)
[![Prisma CLI](https://img.shields.io/badge/prisma-7.10%2B-5A67D8.svg)](https://www.prisma.io/)
[![API](https://img.shields.io/badge/api-Tenrai%20API%20v1-10b981.svg)](https://api.tenrai.org/documentation)

---

### Metadatos del Repositorio de GitHub

> **Description:**  
> Plataforma interactiva de Manga, Anime y Novelas Ligeras desarrollada en Django puro con Prisma Postgres, Tenrai API v1, Taller de Escritores y CI/CD automatizado.
>
> **Website:**  
> `https://growup-7my7.onrender.com`
>
> **Topics:**  
> `anime`, `cicd`, `django`, `github-actions`, `light-novels`, `manga`, `prisma-postgres`, `python`, `render`, `tenrai-api`

---

## Despliegue en la Nube 100% Autonomo (Render Web Service)

La aplicacion se ejecuta de forma completamente autonoma en **Render** sin requerir ninguna sesion ni ejecucion local en la computadora del desarrollador:

- **Instancia en Produccion:** [https://growup-7my7.onrender.com](https://growup-7my7.onrender.com)
- **Base de Datos Cloud:** Prisma Postgres alojada en la nube (`pooled.db.prisma.io:5432`) con pooling de conexiones y SSL requerido.
- **Entrega de Archivos Estaticos:** Integracion con **WhiteNoise** (`CompressedStaticFilesStorage`) para compresion Brotli/Gzip y cache instantaneo de 137 assets.
- **Servidor WSGI/ASGI Concurrente:** Soporte dual para **Gunicorn** y **Uvicorn** gestionando peticiones HTTP y WebSockets en tiempo real.
- **Resiliencia ante Caidas de API Externa (Tenrai API v1):** Mecanismo de contingencia con catalogo semilla pre-registrado en memoria para asegurar que animes, mangas y novelas siempre se muestren incluso ante demoras o limites de tasa de servidores externos.

---

## Caracteristicas Principales del Sistema

1. **Catalogo Multimedial y Landing Page Dinamica (Tenrai API v1):**
   - Sincronizacion directa con el catalogo oficial de MyAnimeList.
   - Exploracion filtrable de Animes, Mangas, Novelas Ligeras y Obras de la Comunidad con paginacion de 24 registros por pagina.
   - Seccion detallada de cada obra con enlaces a plataformas oficiales (Crunchyroll, Netflix, MANGA Plus, BookWalker) y comunitarias (AnimeFLV, MangaDex, TuNovelaLigera).
   - Botones para compartir enlaces directamente en WhatsApp, Facebook, X, Telegram, Email y copiado al portapapeles.

2. **Sistema de Notificaciones en Tiempo Real via WebSockets:**
   - Conexion asincrona a `/ws/live/` sin sobrecarga de consultas recurrentes a la base de datos.
   - Notificaciones emergentes (*pop-ups*) flotantes independientes del contenido, con temporizador de 5 segundos y barra de progreso.
   - Botones e indicadores en la barra superior (*topbar*) junto a las opciones de navegacion del usuario:
     - **Calificaciones y Resenas:** Icono de estrella dorada (`bi-star-fill text-warning`), informando calificaciones recibidas en novelas (autores) o repercusion de opiniones (lectores).
     - **Preguntas, Respuestas y Debates:** Icono de chat interactivo (`bi-chat-left-dots-fill text-info`), informando respuestas y nuevos comentarios en foros seguidos.

3. **Workspace y Panel de Usuario Diferenciado por Roles:**
   - **Rol Lector:** Dashboard personal con metricas de obras guardadas, historial de opiniones formuladas y debates activos.
   - **Rol Escritor / Autor:** Dashboard con desglose de novelas publicadas, calificaciones promedio recibidas de los lectores y gestion de capitulos.
   - **Filtros por URL (`?filtro=`):** Filtrado rapido por cantidad de estrellas (1 a 5) o por tipo de medio con badges visuales interactivos.
   - **Edicion de Perfil en Ventana Modal:** Formulario dinamico alojado en `#editProfileModal` que preserva visible la ficha de identidad del usuario.

4. **Taller de Escritores de Novelas Ligeras:**
   - Creacion de novelas con titulo, sinopsis, portada personalizada y generos.
   - Gestion de capitulos con control de estado (Borrador / Publicado).
   - Registro de fechas: creacion, publicacion y ultima actualizacion, con visibilidad publica selectiva para lectores y completa para el autor.

5. **Diseno Visual Profesional:**
   - Paleta Obsidian Cyberpunk con glassmorphism y modo oscuro nativo.
   - Layout fluido de ancho completo (*full-width fluid*) sin margenes restringidos.
   - Ausencia total de emojis en interfaz, plantillas y documentacion, utilizando exclusivamente tipografia e iconos tecnicos SVG / Bootstrap Icons.

6. **Explorador Interactivo de 94 Endpoints GET de Tenrai API v1:**
   - Panel interactivo integrado en el detalle de obras (`item_detail.html`) para consultar y verificar en vivo los 94 endpoints GET oficiales de Tenrai API v1.
   - Categorias filtrables: Anime, Manga, Personajes, Personas, Temporadas, Top, Noticias/Articulos, Productores y Varios.
   - Visualizacion dual: modo visual adaptado (tarjetas para episodios, personajes, imagenes, staff, estadisticas) y modo Raw JSON con inspector y copiado al portapapeles.

7. **Sistema Editorial y Blog Comunitario:**
   - Publicacion, modificacion y eliminacion de articulos de blog restringida exclusivamente a administradores y superusuarios autorizados (`Anmigz`).
   - Zona de comentarios comunitarios activa para que los usuarios autenticados participen y debatan en los articulos publicados.

---

## Arquitectura Tecnica

```mermaid
flowchart TD
    Client["Navegador Web / Cliente"] -->|HTTPS / WSS| Render["Render Web Service (growup-7my7)"]
    Render --> Static["WhiteNoise (Static Assets)"]
    Render --> WSGI["Django 6.1 WSGI / ASGI Router"]
    WSGI --> CloudDB[("Prisma Postgres Cloud DB")]
    WSGI --> TenraiService["Tenrai Service (Cache + 94 Endpoints)"]
    TenraiService --> TenraiAPI["Tenrai API v1 (api.tenrai.org/v1)"]
```

---

## Variables de Entorno Requeridas (.env)

```env
DEBUG=False
SECRET_KEY=tu-clave-secreta-de-django
ALLOWED_HOSTS=*
DATABASE_URL=postgres://usuario:password@pooled.db.prisma.io:5432/postgres?sslmode=require
TENRAI_API_BASE_URL=https://api.tenrai.org/v1
TENRAI_SERVER_KEY=
JWT_ACCESS_MINUTES=60
JWT_REFRESH_DAYS=7
PYTHON_VERSION=3.12.10
```

---

## Comandos de Compilacion y Ejecucion en Render

- **Build Command:**
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```
- **Start Command (Uvicorn ASGI con WebSockets):**
  ```bash
  uvicorn growup.asgi:application --host 0.0.0.0 --port $PORT
  ```
  *O alternativamente con Gunicorn:*
  ```bash
  gunicorn growup.wsgi:application
  ```

---

## Suite de Pruebas Automatizadas

El proyecto incluye pruebas unitarias exhaustivas que cubren modelos, vistas, catalogo Tenrai API v1, endpoints de WebSockets y permisos de roles:

```bash
python manage.py test
```

Todas las pruebas se ejecutan de forma aislada en GitHub Actions en cada Pull Request.
