# myapp/context_processors.py

from .models import CartItem
from .forms import SubscribeForm

def global_context(request):
    return {
        'subscribe_form': SubscribeForm()
    }

def cart_item_count(request):
    """Return the total quantity of items in the user's cart."""
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_count = sum(item.quantity for item in cart_items)
        return {'cart_item_count': total_count}
    return {'cart_item_count': 0}
