# Generated by Django 4.1.6 on 2023-02-24 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_todolist_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='date_deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
