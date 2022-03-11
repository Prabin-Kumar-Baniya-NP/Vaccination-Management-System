# Generated by Django 4.0.2 on 2022-03-11 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0003_rename_available_quantity_storage_total_quantity'),
        ('vaccine', '0001_initial'),
        ('vaccination', '0004_remove_vaccinationdate_slots_slot_vaccination_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VaccinationDate',
            new_name='Vaccination_Campaign',
        ),
        migrations.RenameField(
            model_name='slot',
            old_name='vaccination_date',
            new_name='campaign',
        ),
        migrations.RenameField(
            model_name='vaccination',
            old_name='date',
            new_name='campaign',
        ),
    ]
