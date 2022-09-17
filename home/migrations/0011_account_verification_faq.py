# Generated by Django 3.2.7 on 2021-09-13 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0010_problem_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, unique=True)),
                ('short_title', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('text', models.TextField()),
                ('priority', models.IntegerField(unique=True)),
                ('active', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('last_modified_data', models.DateField(auto_now=True)),
                ('last_modified_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='account_verification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verification_code', models.CharField(max_length=100, unique=True)),
                ('verification_link', models.URLField(max_length=300, unique=True)),
                ('verification_status', models.BooleanField(choices=[(True, 'verified'), (False, 'Not verified')], default=False)),
                ('account_status', models.BooleanField(choices=[(True, 'Active account'), (False, 'Blocked account')], default=False)),
                ('last_modified_data', models.DateField(auto_now=True)),
                ('last_modified_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]