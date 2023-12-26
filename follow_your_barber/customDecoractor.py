from functools import wraps
from django.http import JsonResponse
from users.models import User
from classes.TokenManager import token_manager

def status_required(account_status_list, email_status_list, phone_number_list):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                access_token = request.COOKIES.get("access_token")
                user_id = token_manager.get_data("id", access_token, "ACCESS")

                user_from_db = User.objects.filter(id=user_id).values("account_status", "email_status", "phone_number_status")[0]

                if user_from_db["account_status"] not in account_status_list and account_status_list!= [""]:
                    return JsonResponse({"message": f"Account status should be one of : {account_status_list} for route {request.path_info}"}, status=403)

                if user_from_db["email_status"] not in email_status_list and email_status_list != [""]:
                    return JsonResponse({"message": f"Email status should be one of : {email_status_list} for route {request.path_info}"}, status=403)

                #if user_from_db["phone_number_status"] not in phone_number_list:
                    #return JsonResponse({"message": f"Phone number status should be one of : {phone_number_list} for route {request.path_info}"}, status=403)

                return view_func(request, *args, **kwargs)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        return wrapper
    return decorator

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try : 
                access_token = request.COOKIES.get("access_token")
                user_role = token_manager.get_data("role", access_token, "ACCESS")

                if user_role == "ADMIN" or user_role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                
                return JsonResponse({"message": "Missing rights."}, status=403)
            except Exception as e :
                return JsonResponse({"error": str(e)}, status=500)
        return wrapper
    return decorator

def owner_required():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, user_id, *args, **kwargs):
            try : 
                access_token = request.COOKIES.get("access_token")
                current_user_id = token_manager.get_data("id", access_token, "ACCESS")
                user_role = token_manager.get_data("role", access_token, "ACCESS")
            
                if current_user_id != user_id or user_role != "ADMIN" : 
                    return JsonResponse({"message": "User is not the owner of the resource."}, status=403)
           
                return view_func(request, user_id, *args, **kwargs)
            except Exception as e :
                return JsonResponse({"error": str(e)}, status=500)
        return wrapper
    return decorator