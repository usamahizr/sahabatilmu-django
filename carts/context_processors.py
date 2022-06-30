from .models import Cart, CartItem
from .views import _cart_id #"from . import" maksudnya die refer to views on current directory which is []cart, x macam atas die merentasi directory lain....sekali run error sebab x mention view daaa


def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {} #return empty dictionory "{}" if we are on admin, we will not see anything there
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))    # "cart_id(request)" mempunyai session id
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity # cart_count kene initialize = 0 dekat
        except Cart.DoesNotExist:          # =========================== sekiranya cart does not exist==========================================
            cart_count = 0
    return dict(cart_count=cart_count)
