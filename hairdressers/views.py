from django.http import JsonResponse

def get_schedule(request):
    return JsonResponse({"payload": "P"}, status=200)