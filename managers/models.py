from django.db import models
from users.models import User

class Manager(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, db_column='user_id')

    class Meta:
        db_table = 'manager'
    
    def __str__(self):
        return f"Manager {self.UserID}"
    
class ManagerSubscription(models.Model):
    manager_id = models.ForeignKey(Manager, on_delete=models.CASCADE, db_column='manager_id')
    amount = models.DecimalField(max_digits=10, decimal_places=2, choices=((25, '25 per month'),(50, '50 per month'),(80, '80 per month')))
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'manager_subscription'