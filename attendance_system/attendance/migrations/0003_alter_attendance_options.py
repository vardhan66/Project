# Generated by Django 5.1.4 on 2025-01-20 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_remove_student_roll_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={'ordering': ['-date', 'time_in']},
        ),
    ]
