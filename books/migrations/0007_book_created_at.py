# Generated by Django 5.1 on 2024-10-20 08:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_book_added_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]