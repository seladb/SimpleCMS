# Generated by Django 3.0.7 on 2020-06-16 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SimpleCmsAPI', '0003_auto_20200615_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]