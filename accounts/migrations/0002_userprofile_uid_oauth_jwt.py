import uuid
from django.db import migrations, models


def gen_uuid(apps, schema_editor):
    UserProfile = apps.get_model('accounts', 'UserProfile')
    for profile in UserProfile.objects.all():
        if not profile.uid:
            profile.uid = uuid.uuid4()
            profile.save(update_fields=['uid'])


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='userprofile',
            name='uid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='oauth_provider',
            field=models.CharField(blank=True, help_text='Proveedor OAuth 2.0 (google, github)', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='oauth_uid',
            field=models.CharField(blank=True, help_text='Identificador de usuario en OAuth 2.0', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='jwt_token_version',
            field=models.IntegerField(default=1, help_text='Version de token para revocacion de JWT'),
        ),
    ]
