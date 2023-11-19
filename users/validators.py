from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import django.contrib.auth.password_validation as password_validators
from phonenumbers.phonenumberutil import parse, is_valid_number

def is_valid_phone_number(phone_number, default_region='FR'):
    try:
        parsed_number = parse(phone_number, default_region)
        if not is_valid_number(parsed_number):
            raise ValidationError("Invalid phone number")
    except ValidationError as e:
        raise ValidationError("Invalid phone number")

def is_valid_password(password):
    try:
        password_validators.validate_password(password=password)
    except ValidationError as e:
        raise ValidationError("Invalid password")

def is_valid_email(email):
    try:
        email_validator = EmailValidator()
        email_validator(str(email).upper())
    except ValidationError as e:
        raise ValidationError("Invalid email")
