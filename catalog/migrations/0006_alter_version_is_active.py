# Generated by Django 4.2 on 2024-04-30 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_version_product_alter_version_version_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активная версия'),
        ),
    ]
