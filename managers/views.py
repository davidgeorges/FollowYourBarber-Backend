from django.http import JsonResponse

def get_employees(request):
    return JsonResponse({"payload": "P"}, status=200)