# Generated by Django 3.2.7 on 2021-09-11 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210911_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='slug',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
