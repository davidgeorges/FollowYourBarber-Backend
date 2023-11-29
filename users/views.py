from django.http import JsonResponse
from classes.TokenManager import token_manager
from follow_your_barber.customDecoractor import access_denied_if_status
from .models import User
from django.core import serializers
import logging

logger = logging.getLogger('django')

@access_denied_if_status(["SUSPENDED"],[""],[""])
def get_account_details(request):
    try :

        access_token = request.COOKIES.get("access_token")
        user_id = token_manager.get_data("id", access_token, "ACCESS")

        if user_id is None:
            return JsonResponse({"error": "Internal server error."}, status=500)
        
        user_from_db = User.objects.get(id=user_id)
        user_data = serializers.serialize('json', [user_from_db])

        return JsonResponse({"payload": user_data}, status=200)
    
    except User.DoesNotExist :
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e :
        logger.error("An error occurred in the users.get_user", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)