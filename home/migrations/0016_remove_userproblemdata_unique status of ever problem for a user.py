# Generated by Django 3.2.7 on 2021-09-13 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20210913_2303'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userproblemdata',
            name='unique status of ever problem for a user',
        ),
    ]
