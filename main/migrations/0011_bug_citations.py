# Generated by Django 4.2 on 2023-04-20 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_species_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='citations',
            field=models.TextField(default='Citations go here'),
            preserve_default=False,
        ),
    ]
