from django.shortcuts import get_object_or_404, render
from .models import Banner
from cart.forms import CartAddProductForm
from .models import Category, Product
from .recommender import Recommender


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(parent__isnull=True)  # Fetch root categories
    products = Product.objects.filter(available=True)
    banners = Banner.objects.all()  # Fetch banners
    

    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)  # Search by product name


    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
            'banners': banners,  # Pass banners to the template

        },
    )


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product, id=id, slug=slug, available=True
    )
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product,
            'cart_product_form': cart_product_form,
            'recommended_products': recommended_products,
        },
    )



