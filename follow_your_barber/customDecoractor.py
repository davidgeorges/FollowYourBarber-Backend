from functools import wraps
from django.http import JsonResponse
from users.models import User
from classes.TokenManager import token_manager

def access_denied_if_status(account_status_list,email_status_list,phone_number_list):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try : 
                access_token = request.COOKIES.get("access_token")
                user_id = token_manager.get_data("id", access_token, "ACCESS")
                user_from_db = User.objects.filter(id=user_id).values("account_status", "email_status", "phone_number_status")[0]
                
                if user_from_db["account_status"] in account_status_list:
                    return JsonResponse({"message": f"Account status should not be one of : {account_status_list} for route {request.path_info}"}, status=403)
                
                if user_from_db["email_status"] in email_status_list:
                    return JsonResponse({"message": f"Email status should not be one of : {email_status_list} for route {request.path_info}"}, status=403)

                #if user_from_db["phone_number_status"] in phone_number_list:
                    #return JsonResponse({"message": f"Phone number status should not be one of : {phone_number_list} for route {request.path_info}"}, status=403)

                return view_func(request, *args, **kwargs)
            except Exception as e :
                return JsonResponse({"error": str(e)}, status=500)
        return wrapper
    return decorator