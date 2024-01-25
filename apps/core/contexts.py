from .models import Category
from apps.sellers.models import Seller


def category(request):
    categories = Category.objects.all().order_by('name')
    return {"categories": categories}

def seller(request):
    sellers = Seller.objects.all().order_by('rank')
    return {"sellers": sellers}
