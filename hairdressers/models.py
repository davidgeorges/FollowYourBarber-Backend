from django.db import models
from hair_salons.models import HairSalon
from users.models import User

class Hairdresser(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, db_column='user_id')
    hair_salon_id = models.ForeignKey(HairSalon, on_delete=models.CASCADE, db_column='hair_salon_id')

    class Meta:
            db_table = 'hairdresser'

    def __str__(self):
        return f"Hairdresser {self.UserID}"
