# Generated by Django 4.2.1 on 2023-05-18 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('School_Admin', '0002_remove_courseinformations_time_required_to_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseinformations',
            name='departement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='School_Admin.department'),
        ),
    ]
