from .models import Category
# Create your views here.

def categories (request):
    return {
        'categories': Category.objects.filter(level=0)
    }
