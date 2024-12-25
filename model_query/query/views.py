from django.http import JsonResponse
from .queries import get_top_categories

# Create your views here.

def top_categories_view(request):
    result = get_top_categories()
    return JsonResponse(result, safe=False)
