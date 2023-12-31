# Generated by Django 4.2.6 on 2023-11-10 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_user_refresh_token'),
        ('managers', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='HairSalon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address_id', models.ForeignKey(db_column='address_id', on_delete=django.db.models.deletion.CASCADE, to='users.address')),
                ('manager_id', models.ForeignKey(db_column='manager_id', on_delete=django.db.models.deletion.CASCADE, to='managers.manager')),
            ],
            options={
                'db_table': 'hair_salon',
            },
        ),
        migrations.CreateModel(
            name='ManagerHairSalon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hair_salon_id', models.ForeignKey(db_column='hair_salon_id', on_delete=django.db.models.deletion.CASCADE, to='hair_salons.hairsalon')),
                ('manager_id', models.ForeignKey(db_column='manager_id', on_delete=django.db.models.deletion.CASCADE, to='managers.manager')),
            ],
            options={
                'db_table': 'manager_hair_salon',
            },
        ),
    ]
