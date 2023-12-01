from django.forms import ValidationError
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.db import transaction
from users.models import Address, User
from authentification.models import RefreshToken
from classes.TokenManager import token_manager
from classes.PasswordManager import password_manager
from classes.MailManager import mail_manager
import json
import logging

logger = logging.getLogger('django')

@require_http_methods(["POST"])
def login(request):
    try:
        with transaction.atomic():
            user_from_body = json.loads(request.body) 
            user_from_db = list(User.objects.filter(email=str(user_from_body["email"]).upper()).values("id", "first_name", "last_name", "account_status", "password_hash","role", "refresh_token"))

            if len(user_from_db) <= 0 : 
                return JsonResponse({"error": "User not found."}, status=404)
            
            if not password_manager.verify_password(user_from_body["password"],user_from_db[0]["password_hash"]) :
                return JsonResponse({"message": "Wrong credentials."},status=401)
            
            user_from_body["password"] = None
            
            if user_from_db[0]["account_status"] in ("INACTIVE", "SUSPENDED") : 
                return JsonResponse({"message": f"Account {user_from_db[0]['account_status']}"},status=403)

            if user_from_db[0]["role"] is None : 
                raise Exception("Error in data format.")
            
            if user_from_db[0]["refresh_token"] is not None :
                RefreshToken.objects.get(pk=user_from_db[0]["refresh_token"]).delete()
                
            access_token = "Bearer "+token_manager.create_token(user_from_db[0]["id"], user_from_db[0]["role"], user_from_db[0]["account_status"], "ACCESS")
            refresh_token = "Bearer "+token_manager.create_token(user_from_db[0]["id"], user_from_db[0]["role"], user_from_db[0]["account_status"], "REFRESH")

            refresh_token_in_db = RefreshToken.create_with_user_id(refresh_token, email=user_from_body["email"].upper())
            refresh_token_in_db.save()
    
            User.objects.filter(email=str(user_from_body["email"]).upper()).update(refresh_token=refresh_token_in_db)

            response = JsonResponse({"message" :"User connected with success.", "id":user_from_db[0]["id"], "role" : user_from_db[0]["role"], "accountStatus" : user_from_db[0]["account_status"]},status=200)
            response.set_cookie(key="access_token",value=access_token,httponly=True)
            response.set_cookie(key="refresh_token",value=refresh_token,httponly=True)
        
            return response 
    except Exception as e : 
        logger.error("An error occurred in the authentification.login", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)

@require_http_methods(["POST"])
def logout(request):
    try :
        response = JsonResponse({"message" : "User disconnected with success."},status=200)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.delete_cookie("csrftoken")
        return response
    except Exception as e : 
            logger.error("An error occurred in the authentification.logout", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)

@require_http_methods(["POST"])
def register(request):
    try:
        with transaction.atomic():
            data = json.loads(request.body)

            user_data = data.get("user", {})
            data = None
            
            user_data["password_hash"] = password_manager.create_hash_password(user_data["password_hash"])
            address_data = user_data.pop("address_id", {})

            address = Address(**address_data)
            address.data_to_upper()
            address.full_clean()
            address.save()
            
            user = User(address_id=address, role="CUSTOMER", **user_data)
            user.data_to_upper()
            user.full_clean()
            user.save()

            return JsonResponse({"message": "User registered successfully"})
    except ValidationError as e :
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error("An error occurred in the authentification.register", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)
    
@require_http_methods(["POST"])
def send_verification_mail(request, user_id):
    try:
        user_from_db = list(User.objects.filter(id=user_id).values("first_name","email"))

        if len(user_from_db) <= 0 : 
            return JsonResponse({"error": "User not found."}, status=404)
        
        mail_manager.send_verification_mail(user_from_db[0]['first_name'],user_from_db[0]['email'])
        
        return JsonResponse({"message": "Mail send successfully"}, status=200)
    except Exception as e : 
        logger.error("An error occurred in the authentification.login", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)   

@require_http_methods(["GET"])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrf_token": csrf_token})

    