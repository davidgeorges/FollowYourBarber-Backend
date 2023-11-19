from django.db import models
from users.validators import *

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    street_address = models.CharField(max_length=255, null=False, blank=False)
    zip_code = models.CharField(max_length=10, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    region = models.CharField(max_length=50, null=False, blank=False)

    def data_to_upper(self):
        self.street_address = self.street_address.upper()
        self.zip_code = self.zip_code.upper()
        self.city = self.city.upper()
        self.region = self.region.upper()

    class Meta:
            db_table = 'address'

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.region} {self.zip_code}"

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50 ,null=False, blank=False,)
    last_name = models.CharField(max_length=50 ,null=False, blank=False,)
    email = models.CharField(max_length=100, unique=True,null=False, blank=False, validators=[is_valid_email])
    password_hash = models.CharField(max_length=256, null=False, blank=False, validators=[is_valid_password])
    phone_number = models.CharField(max_length=15, unique=True, null=False, blank=False, validators=[is_valid_phone_number])
    account_status = models.CharField(max_length=30, choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE'), ('SUSPENDED', 'SUSPENDED'), ('PENDING', 'PENDING'), ('EMAIL_PENDING', 'EMAIL_PENDING'), ('PHONE_PENDING', 'PHONE_PENDING'), ('EMAIL_AND_PHONE_PENDING', 'EMAIL_AND_PHONE_PENDING')], default='EMAIL_AND_PHONE_PENDING', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.OneToOneField('authentification.refreshtoken', on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, default='CUSTOMER',  null=False, blank=False)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE, db_column='address_id')
    
    def data_to_upper(self):
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        self.email = self.email.upper()

    class Meta:
            db_table = 'user'

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.address_id}"
    
