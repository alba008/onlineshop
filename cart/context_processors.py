from .cart import Cart
def cart(request):
    return {'cart': Cart(request)}


def cart_items_count(request):
    cart = Cart(request)
    return {"cart_items_count": len(cart)}
