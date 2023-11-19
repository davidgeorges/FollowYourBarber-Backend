from django.http import HttpResponse
from .models import User

# Create your views here.

def index(request):
    user_from_db = User.objects.all()
    print(user_from_db)
    return HttpResponse(f"Hello, world. You're at the polls index.{user_from_db}")

