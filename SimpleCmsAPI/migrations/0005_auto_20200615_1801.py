# Generated by Django 3.0.7 on 2020-06-16 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SimpleCmsAPI', '0004_auto_20200615_1713'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('added_by', 'blog_post')},
        ),
    ]