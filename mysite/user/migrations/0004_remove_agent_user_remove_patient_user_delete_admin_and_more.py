# Generated by Django 4.0.4 on 2022-06-09 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_patient_blood_group_user_blood_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='user',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='user',
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='Agent',
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
    ]
