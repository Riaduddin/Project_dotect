from django.db.models import Sum, Count, F
from django.http import JsonResponse
from api.category.models import Category

def get_top_categories():
    """
    Retrieves the top 5 categories by total product price.
    Returns a list of dictionaries containing category name, total price, and product count.
    """
    return list(Category.objects
        .annotate(
            total_price=Sum('product__price'),
            product_count=Count('product')
        )
        .filter(product_count__gt=0)
        .values(
            'name',
            'total_price',
            'product_count'
        )
        .order_by('-total_price')
        .annotate(
            category_name=F('name')
        )
        .values(
            'category_name',
            'total_price',
            'product_count'
        )[:5])


def top_categories_view(request):
    """API endpoint to get top categories"""
    return JsonResponse(get_top_categories(), safe=False)