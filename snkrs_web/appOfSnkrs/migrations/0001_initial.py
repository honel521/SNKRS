# Generated by Django 2.1.2 on 2018-11-04 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=11, unique=True)),
                ('password', models.CharField(max_length=64)),
                ('addr', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=64)),
                ('size', models.CharField(max_length=32, null=True)),
            ],
        ),
    ]
