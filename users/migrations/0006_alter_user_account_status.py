# Generated by Django 4.2.6 on 2023-11-12 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_password_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_status',
            field=models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE'), ('SUSPENDED', 'SUSPENDED'), ('PENDING', 'PENDING'), ('EMAIL_PENDING', 'EMAIL_PENDING'), ('PHONE_PENDING', 'PHONE_PENDING'), ('EMAIL_AND_PHONE_PENDING', 'EMAIL_AND_PHONE_PENDING')], default='EMAIL_AND_PHONE_PENDING', max_length=30),
        ),
    ]
