from django.db import models
from users.models import Address
from managers.models import  Manager

class HairSalon(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE, db_column='address_id')
    manager_id = models.ForeignKey(Manager, on_delete=models.CASCADE, db_column='manager_id')

    class Meta:
            db_table = 'hair_salon'

    def __str__(self):
        return self.Name
    
class ManagerHairSalon(models.Model):
    manager_id = models.ForeignKey(Manager, on_delete=models.CASCADE, db_column='manager_id')
    hair_salon_id = models.ForeignKey(HairSalon, on_delete=models.CASCADE, db_column='hair_salon_id')

    class Meta:
            db_table = 'manager_hair_salon'

    
