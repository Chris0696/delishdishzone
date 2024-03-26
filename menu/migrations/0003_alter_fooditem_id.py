# Generated by Django 4.2.10 on 2024-03-14 20:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_fooditem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]