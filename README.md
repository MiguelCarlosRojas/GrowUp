# GrowUp - Plataforma de Manga, Anime y Novelas Ligeras

[![CI Compilation & Test Suite](https://github.com/MiguelCarlosRojas/GrowUp/actions/workflows/ci.yml/badge.svg)](https://github.com/MiguelCarlosRojas/GrowUp/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.1%2B%20%7C%206.1-green.svg)](https://www.djangoproject.com/)
[![Database](https://img.shields.io/badge/database-Prisma%20Postgres-3963F7.svg)](https://www.prisma.io/postgres)
[![Prisma CLI](https://img.shields.io/badge/prisma-7.10%2B-5A67D8.svg)](https://www.prisma.io/)
[![API](https://img.shields.io/badge/api-Jikan%20API%20v4-2e51a2.svg)](https://jikan.moe/)

---

### Metadatos del Repositorio de GitHub

> **Description:**  
> Plataforma interactiva de Manga, Anime y Novelas Ligeras desarrollada en Django puro con Prisma Postgres, Jikan API v4, Taller de Escritores, sistema de reseñas y CI/CD automatizado con GitHub Actions.
>
> **Website:**  
> `https://growup-anime.vercel.app`
>
> **Topics:**  
> `django`, `python`, `anime`, `manga`, `light-novels`, `jikan-api`, `prisma-postgres`, `github-actions`, `cicd`, `web-development`, `postgresql`

---

## Caracteristicas Principales

1. **Diseño Visual Ultra-Profesional:**
   - Estética inspirada en plataformas como Crunchyroll y AniList con **Glassmorphism**, iluminación ambiental (*ambient glow*) y modo oscuro de alto contraste.
   - **Logotipo SVG Oficial** e icono de pestaña (*favicon*) vectoriales de alta definición.
   - **Custom Scrollbar** con degradado continuo y bordes redondeados.
   - **Disposición de Ancho Completo (*Full-Width Fluid*):** Diseñada para aprovechar pantallas panorámicas y monitores ultrawide sin márgenes estrechos.
   - **Responsividad Total:** Tipografía fluida `clamp()`, tarjetas con relación de aspecto adaptable (2:3 y 3:4) y paneles táctiles en smartphones.
   - **Lector de Capítulos Inmersivo:** Modos de lectura seleccionables (*Dark*, *Sepia Clásico*, *Negro OLED*), tamaño de letra ajustable y navegación secuencial.

2. **Base de Datos con Prisma Postgres:**
   - Conexión configurada hacia **Prisma Postgres** (`pooled.db.prisma.io:5432`) mediante variables de entorno seguras (`DATABASE_URL`).
   - Soporte para **Prisma CLI** (`npx prisma db pull`, `npx prisma generate`, `npx prisma studio`).
   - Modo de resiliencia con fallback a SQLite local para testing y CI sin dependencias de red externas.

3. **Catálogo & Landing Page Dinámica (Jikan API v4):**
   - Sincronización en tiempo real con MyAnimeList.
   - Obras maestras y estrenos de anime, manga y novelas ligeras oficiales.
   - Filtros avanzados: por medio (*Anime, Manga, Novela Ligera, Obras de la Comunidad*), término de búsqueda, géneros múltiples, estado de emisión y ordenamiento.

4. **Sistema de Clasificación, Opiniones y Discusiones (Q&A):**
   - Calificación interactiva de 1 a 5 con cálculo automático de promedios de la comunidad.
   - Reseñas con título y opinión detallada.
   - Foro de discusión por obra: comentarios y preguntas con respuestas anidadas en hilos.

5. **Taller de Escritores (Novelas Ligeras Originales):**
   - Módulo completo para autores: título, sinopsis, imagen de portada, demografía, idioma y categorías/géneros (*Isekai, Fantasía, Acción, Romance, etc.*).
   - Gestión de capítulos: numeración, título, contenido completo, conteo de palabras y notas del autor.

---

## Herramientas de Prisma Postgres

El proyecto cuenta con soporte para el ecosistema de Prisma:

```bash
# Inspeccionar o sincronizar las tablas de la base de datos
npx prisma db pull

# Generar el cliente de Prisma
npx prisma generate

# Abrir Prisma Studio para explorar la base de datos en el navegador
npx prisma studio
```

---

## Flujo de Ramas & Automatizacion CI/CD con GitHub Actions

```mermaid
flowchart LR
    A["feature/sp*"] -->|Push / Compilacion OK| B["Auto PR a develop"]
    B -->|Merge a develop / Compilacion OK| C["Auto PR a main"]
    C -->|Merge| D["Produccion / main"]
```

---

## Instalacion y Ejecucion Local

### Prerrequisitos
- Python 3.12 o superior.
- Node.js v20+ y npm.
- Git.

### 1. Clonar el repositorio y acceder
```bash
git clone https://github.com/MiguelCarlosRojas/GrowUp.git
cd GrowUp
```

### 2. Crear y activar entorno virtual
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias de Python y Node.js
```bash
pip install -r requirements.txt
npm install
```

### 4. Configurar Variables de Entorno
Copia la plantilla `.env.example` a `.env`:
```bash
cp .env.example .env
```
Edita `.env` con tus credenciales de Prisma Postgres o PostgreSQL y la configuración de Jikan API v4:

```env
DATABASE_URL=postgresql://...
JIKAN_API_BASE_URL=https://api.jikan.moe/v4
JIKAN_API_TIMEOUT=6
JIKAN_CACHE_TTL=900
JIKAN_TOP_LIMIT=12
JIKAN_SEARCH_LIMIT=18
```

### 5. Aplicar migraciones y datos iniciales
```bash
python manage.py migrate
python manage.py seed_categories
```

### 6. Ejecutar pruebas unitarias
```bash
python manage.py test
```

### 7. Iniciar el servidor de desarrollo
```bash
python manage.py runserver
```
Accede en tu navegador a: `http://127.0.0.1:8000/`

---

## Licencia y Conducta
Consulta [COPYRIGHT.md](COPYRIGHT.md) y [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) para más detalles.
