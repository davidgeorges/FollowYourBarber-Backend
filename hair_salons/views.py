from django.http import JsonResponse
from follow_your_barber.customDecoractor import access_denied_if_status
from classes.TokenManager import token_manager
from users.models import User
from django.core import serializers
import logging

logger = logging.getLogger('django')

@access_denied_if_status(["SUSPENDED"],[""],[""])
def get_hair_salons(request):
    try: 
        return JsonResponse({"payload": "user_data"}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        logger.error("An error occurred in the users.get_user", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)
    
@access_denied_if_status(["SUSPENDED"],[""],[""])
def get_hair_salon(request, hair_salon_id):
    try: 
        print(hair_salon_id)
        return JsonResponse({"payload": "user_data"}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        logger.error("An error occurred in the users.get_user", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)