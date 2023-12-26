
from django.http import JsonResponse
from classes.TokenManager import token_manager
import logging

logger = logging.getLogger('django')

def token_filter(get_response):
    
    def middleware(request):

        request_splited = request.path.split("/")
        if "auth" in request_splited and "sendVerificationMail" not in request_splited and "refreshToken" not in request_splited:
            return get_response(request)
        
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token is None:
                return JsonResponse({"message": "User not authentificated."}, status=401)
            
            if token_manager.check_if_is_expired(refresh_token, "REFRESH"):
                return JsonResponse({"message": "Refresh token is expired."}, status=401)
            
            access_token = request.COOKIES.get("access_token")
            if access_token is None:
                return JsonResponse({"message": "Missing access token."}, status=401)
            
            if token_manager.check_if_is_expired(access_token, "ACCESS"):
                return JsonResponse({"message": "Access token is expired."}, status=401)

            return get_response(request)
        except Exception as e:
            logger.error("An error occurred in the middleware.token_filter", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)

    return middleware
