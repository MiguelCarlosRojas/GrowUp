import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('reader', 'Lector'),
        ('author', 'Escritor / Autor'),
    ]

    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')
    bio = models.TextField(blank=True, max_length=500, help_text="Biografía corta del usuario")
    avatar_url = models.URLField(blank=True, default="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150")
    favorite_genres = models.CharField(max_length=255, blank=True, help_text="Géneros favoritos separados por comas")
    
    # OAuth 2.0 and JWT Tracking
    oauth_provider = models.CharField(max_length=50, blank=True, null=True, help_text="Proveedor OAuth 2.0 (google, github)")
    oauth_uid = models.CharField(max_length=150, blank=True, null=True, help_text="Identificador de usuario en OAuth 2.0")
    jwt_token_version = models.IntegerField(default=1, help_text="Version de token para revocacion de JWT")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.uid}) [{self.get_role_display()}]"

    @property
    def is_author(self):
        return self.role == 'author' or self.user.is_staff


# Helper property on User to access uid directly
if not hasattr(User, 'uid'):
    User.add_to_class('uid', property(lambda u: str(u.profile.uid) if hasattr(u, 'profile') and u.profile.uid else ''))


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()

