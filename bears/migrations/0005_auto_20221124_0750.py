# Generated by Django 3.1.3 on 2022-11-24 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bears', '0004_sighting_deploy_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bear',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sighting',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]