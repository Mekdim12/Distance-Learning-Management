# Generated by Django 4.2.1 on 2023-05-23 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentInformation',
            fields=[
                ('userid', models.CharField(db_column='UserId', max_length=104, primary_key=True, serialize=False)),
                ('firstname', models.CharField(db_column='FirstName', max_length=100)),
                ('middlename', models.CharField(db_column='MiddleName', max_length=100)),
                ('lastname', models.CharField(db_column='LastName', max_length=100)),
                ('age', models.IntegerField(db_column='Age')),
                ('country', models.CharField(db_column='Country', max_length=100)),
                ('woredazone', models.CharField(db_column='WoredaZone', max_length=100)),
                ('streetkebele', models.CharField(db_column='StreetKebele', max_length=100)),
                ('phonenumber', models.CharField(blank=True, db_column='PhoneNumber', max_length=100, null=True)),
                ('profilePicture', models.ImageField(db_column='profilePicture', upload_to='Images/')),
                ('disability', models.CharField(max_length=132, null=True)),
                ('jobtype', models.CharField(max_length=132, null=True)),
                ('student_cv_pdf_file', models.FileField(upload_to='Files/')),
                ('email', models.EmailField(max_length=55, null=True)),
                ('is_photos_taken', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'StudentInformation',
                'unique_together': {('firstname', 'userid', 'middlename', 'lastname')},
            },
        ),
    ]