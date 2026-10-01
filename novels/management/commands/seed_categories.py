from django.core.management.base import BaseCommand
from novels.models import Category


class Command(BaseCommand):
    help = 'Seeds initial categories and genres for light novels'

    def handle(self, *args, **kwargs):
        categories = [
            ('Isekai', 'Historias de transporte o reencarnación en otro mundo'),
            ('Fantasía', 'Mundos mágicos, dragones, espadas y hechizos'),
            ('Acción', 'Batallas intensas, artes marciales y aventuras épicas'),
            ('Romance', 'Historias de amor, parejas y relaciones conmovedoras'),
            ('Aventura', 'Exploración de mazmorras, viajes y misterios'),
            ('Ciencia Ficción', 'Tecnología futurista, mechas y el ciberespacio'),
            ('Comedia', 'Momentos divertidos, parodias y situaciones cómicas'),
            ('Drama', 'Conflictos emocionales y crecimiento de personajes'),
            ('Misterio / Psicológico', 'Juegos mentales, acertijos e intriga'),
            ('Recuentos de la Vida', 'Viviendo el día a día en academias o pueblos'),
        ]

        count = 0
        for name, desc in categories:
            obj, created = Category.objects.get_or_create(name=name, defaults={'description': desc})
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} new categories.'))
