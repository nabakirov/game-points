# Generated by Django 3.0.7 on 2020-06-16 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='interests',
            field=models.TextField(blank=True, null=True, verbose_name='interests'),
        ),
    ]