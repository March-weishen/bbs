# Generated by Django 2.2.1 on 2019-09-27 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(through='app01.Article2Tag', to='app01.Tag'),
        ),
    ]
