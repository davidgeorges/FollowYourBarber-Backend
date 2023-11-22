from functools import wraps
from django.http import JsonResponse
from users.models import User
from classes.TokenManager import token_manager

def verified_status(account_status,email_status,phone_number):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try : 
                access_token = request.COOKIES.get("access_token")
                user_id = token_manager.get_data("id", access_token, "ACCESS")
                user_from_db = User.objects.filter(id=user_id).values("account_status", "email_status", "phone_number_status")[0]

                if user_from_db["account_status"] != account_status:
                    return JsonResponse({"message": f"Account status should be : {account_status} for route {request.path_info}"}, status=403)

                if user_from_db["email_status"] != email_status:
                    return JsonResponse({"message": f"Email status should be : {account_status} for route {request.path_info}"}, status=403)

                if user_from_db["phone_number_status"] != phone_number:
                    return JsonResponse({"message": f"Phone number status should be : {account_status} for route {request.path_info}"}, status=403)

                return view_func(request, *args, **kwargs)
            except Exception as e :
                return JsonResponse({"error": str(e)}, status=500)
        return wrapper
    return decorator
