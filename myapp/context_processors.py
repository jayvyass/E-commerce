# myapp/context_processors.py

from .models import CartItem

def cart_item_count(request):
    """Return the total quantity of items in the user's cart."""
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_count = sum(item.quantity for item in cart_items)
        return {'cart_item_count': total_count}
    return {'cart_item_count': 0}
