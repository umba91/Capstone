# Generated by Django 4.1.7 on 2023-03-28 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_bugattribute'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='species',
            options={'verbose_name_plural': 'Specie'},
        ),
        migrations.AlterField(
            model_name='bug',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.species'),
        ),
        migrations.AlterField(
            model_name='bugattribute',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.species'),
        ),
    ]