# Generated by Django 3.2.7 on 2021-09-11 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_problem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='topic',
        ),
        migrations.AddField(
            model_name='topic',
            name='problem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='home.problem'),
        ),
    ]