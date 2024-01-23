from .models import Category


def category(request):
    categories = Category.objects.all().order_by('name')
    return {"categories": categories}
