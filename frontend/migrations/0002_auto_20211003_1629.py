# Generated by Django 3.0 on 2021-10-03 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='block_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='login_try',
            field=models.IntegerField(default=0),
        ),
    ]