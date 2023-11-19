from django.db import models
from users.models import User

class RefreshToken(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=256, unique=True)
    user_id = models.ForeignKey('users.user', on_delete=models.CASCADE, db_column='user_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'refresh_token'

    def __str__(self):
        return self.token
    
    @classmethod
    def create_with_user_id(cls, token, email):
        user = User.objects.get(email=email)
        return cls(token=token, user_id=user)