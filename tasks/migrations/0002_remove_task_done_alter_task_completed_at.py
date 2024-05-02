# Generated by Django 5.0.4 on 2024-05-02 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='done',
        ),
        migrations.AlterField(
            model_name='task',
            name='completed_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
