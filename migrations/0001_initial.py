# Generated by Django 2.0.4 on 2018-04-20 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=10)),
                ('department', models.CharField(max_length=30)),
                ('speciality', models.CharField(max_length=30)),
            ],
        ),
    ]
