
from django.http import JsonResponse
from classes.TokenManager import token_manager
import logging

logger = logging.getLogger('django')

def token_filter(get_response):
    
    def middleware(request):

        request_splited = request.path.split("/")
        if "auth" in request_splited:
            return get_response(request)
        
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token is None:
                return JsonResponse({"message": "Missing refresh_token."}, status=401)
            
            if token_manager.check_if_is_expired(refresh_token, "REFRESH"):
                return JsonResponse({"message": "Error refresh_token expired."}, status=401)
            
            access_token = request.COOKIES.get("access_token")
            if access_token is None:
                return JsonResponse({"message": "Missing access token."}, status=401)
            
            if token_manager.check_if_is_expired(access_token, "ACCESS"):
                return JsonResponse({"message": "Error access_token expired."}, status=401)

            return get_response(request)
        except Exception as e:
            logger.error("An error occurred in the middleware.token_filter", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)

    return middleware

def authorization_filter(get_response):
    
    def middleware(request):

        request_splited = request.path.split("/")
        print(request.path)
        if "auth" or "hairSalons" in request_splited:
            return get_response(request)
        
        try:
            access_token = request.COOKIES.get("access_token")

            user_role = token_manager.get_data("role", access_token, "ACCESS")
            if user_role is None:
                return JsonResponse({"error": "Internal server error."}, status=500)

            if user_role not in request_splited and user_role != "ADMIN":
                return JsonResponse({"message": "No access - Missing rights."}, status=403)

            return get_response(request)
        except Exception as e:
            logger.error("An error occurred in the middleware.token_filter", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)

    return middleware