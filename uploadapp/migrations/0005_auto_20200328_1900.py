# Generated by Django 2.2.1 on 2020-03-28 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadapp', '0004_auto_20200328_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]