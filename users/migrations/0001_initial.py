# Generated by Django 4.2.6 on 2023-11-10 23:29

from django.db import migrations, models
import django.db.models.deletion
import users.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('street_address', models.CharField(max_length=255)),
                ('zip_code', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100, unique=True, validators=[users.validators.is_valid_email])),
                ('password_hash', models.CharField(max_length=100, validators=[users.validators.is_valid_password])),
                ('phone_number', models.CharField(max_length=15, unique=True, validators=[users.validators.is_valid_phone_number])),
                ('account_status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE'), ('SUSPENDED', 'SUSPENDED'), ('PENDING', 'PENDING')], default='ACTIVE', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(default='CUSTOMER', max_length=20)),
                ('address_id', models.ForeignKey(db_column='address_id', on_delete=django.db.models.deletion.CASCADE, to='users.address')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
