# Generated by Django 3.2.7 on 2021-09-12 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_userproblemdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproblemdata',
            name='completed',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
    ]