# Generated by Django 4.0.4 on 2022-05-26 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ideas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ideas', to=settings.AUTH_USER_MODEL),
        ),
    ]
