from django.http import JsonResponse

def get_hair_salons(request):
    return JsonResponse({"payload": "P"}, status=200)