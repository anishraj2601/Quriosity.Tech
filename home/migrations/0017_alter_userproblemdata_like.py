# Generated by Django 3.2.7 on 2021-09-13 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_remove_userproblemdata_unique status of ever problem for a user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproblemdata',
            name='like',
            field=models.BooleanField(blank=True, choices=[(True, 'Like'), (False, 'Unlike')], null=True),
        ),
    ]
