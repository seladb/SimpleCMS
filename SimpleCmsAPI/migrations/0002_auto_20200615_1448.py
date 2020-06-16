# Generated by Django 3.0.7 on 2020-06-15 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SimpleCmsAPI', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='likes',
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SimpleCmsAPI.User')),
                ('blog_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SimpleCmsAPI.BlogPost')),
            ],
        ),
    ]