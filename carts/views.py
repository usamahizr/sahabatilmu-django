from django.shortcuts import render, redirect,get_object_or_404
from store.models import Product, Variation #dia seru product dalam FILE [=]models.py under FOLDER []store
from .models import Cart, CartItem   #nak bring cart item dan cart juga
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse

def _cart_id(request):    #underscrore belakang cart id tu = private fx.
    cart = request.session.session_key #dia panggil session id untuk cart (session id ni ada dalam cookies --> session ---> content)
    if not cart:   # kalau x dia akan create session
        cart = request.session.create()
    return cart  #akan return cart id
#======================================== fx ADD TO CART ========================================================
def add_cart(request, product_id):    #kat sini die create add_cart fx ..... kemudian dia pass request .....
    current_user = request.user
    product = Product.objects.get(id=product_id)     #get the prodcut
    #if the user is authenticated (dah log in)
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item  #if the colour is red, the colour will be store inside the KEY, the black will be store in the value
                value = request.POST[key]   #request post of the KEY

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

    #kat atas tu kita dah selesai create CART | isu sekarang ni dalam cart tentunya akan ada pelbagai PRODUCT @ sbeagai CART ITEM,, perbincangan sambung kat bawah
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user) #product tu = line 12 @ poduct = Product.objects.get(id=product_id)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                #Increase Cart Item Quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1         # item.quantity += 1  #nak create increament pada item by 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                    item.save()
        else:     #except log = what happen if cart item does not exist...so kite kene buat cart item = 1
            cart_item = CartItem.objects.create( #create() = method
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    #if the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item  #if the colour is red, the colour will be store inside the KEY, the black will be store in the value
                value = request.POST[key]   #request post of the KEY

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))  #dia akan dapatkan/recall cart menggunakan cart_id yang ada pada session
        except Cart.DoesNotExist:   #ini nak handle kalau cart x wujud
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()
    #kat atas tu kita dah selesai create CART | isu sekarang ni dalam cart tentunya akan ada pelbagai PRODUCT @ sbeagai CART ITEM,, perbincangan sambung kat bawah
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart) #product tu = line 12 @ poduct = Product.objects.get(id=product_id)
            #1) existing _variaitons - from Database
            #2) current variaitons  - product_variation list
            #3) item ID - Databse
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                #Increase Cart Item Quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1         # item.quantity += 1  #nak create increament pada item by 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                    item.save()
        else:     #except log = what happen if cart item does not exist...so kite kene buat cart item = 1
            cart_item = CartItem.objects.create( #create() = method
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart') #dia akan reidrect user to CART PAGE bila semua fx. dah selesai
    #redirect tu berasal dari redirect line 1
#======================================== fx DECREMENT CART & DELETE CART ITEM ========================================================
def remove_cart(request, product_id, cart_item_id): #pass reqest & produk id ========================== #remove_cart untuk DECREMENT item============

    product = get_object_or_404(Product, id=product_id)    # "get_object_or_404" maksudnya kalau satu2 object tu wujud dia akan present object tersebut,,,kalau x die akan return  404 gitu
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) #it will bring to cart item
        if cart_item.quantity > 1: #condition nak make sure, x decrement sampai jadi -ve
            cart_item.quantity -= 1 #cart item.quantity (equal to) cart item.quantity minus 1 , it will decvrement it??
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):  #=============================== remove_cart_item untuk REMOVE/DELETE item terus ============
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None): #======================================== fx LOOP INCRCEMENT PRODUK DALAM CART + FORMULAR TAX + GRANDTOTAL= =======================================================
    try:
        tax = 0 #ikutkan tuto dia ada error tu die declare awal2, api aku nye x error sebab aku tambah formatted_tax,  kot atau berkenaan formar decimal
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #we are tacking cart object from _cart_id
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items: #we are looking for the cart item, so that we can take the total each of the cart item using formular below
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = 15  #formular 2% tax asalnya  (2 * total) /100.......lepastu aku saja try buat formula math, eg "(12*15)/100".....die jadi error
        formatted_tax = '{0:.2f}'.format(tax) # guna ajaran gugel tukar format -> https://www.codegrepper.com/code-examples/python/frameworks/django/up+to+2+decimal+places+in+python
        grand_total = total + tax
        formatted_grand_total = '{0:.2f}'.format(grand_total) # tukar format ke 2 decimal point

    except ObjectDoesNotExist:
        pass #kalau object not exist/ x de apa2 berlaku tambahan barang dalam cart , dia just pass/ ignore je

    context = { #context= proses sending all the context/ data to HTML templete  #============================================== CONTEXT UPDATE KE HTML============================================================
        'total'                 : total,
        'quantity'              : quantity,
        'cart_items'            : cart_items,
        'tax'                   : tax,
        'formatted_tax'         : formatted_tax, # untuk tukar format ke 2 decimal point
        'grand_total'           : grand_total,
        'formatted_grand_total' : formatted_grand_total, # untuk tukar format ke 2 decimal point

    }
    return render(request, 'store/cart.html', context) #berdaasrkn kuliah 39 min 1.04 context tu send to the cart page aka FILE [=]cart.html FOLDER []templete......semua maklumat tu akan di update pada "context" dalm line ni


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0 #ikutkan tuto dia ada error tu die declare awal2, api aku nye x error sebab aku tambah formatted_tax,  kot atau berkenaan formar decimal
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #we are tacking cart object from _cart_id
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items: #we are looking for the cart item, so that we can take the total each of the cart item using formular below
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = 15  #formular 2% tax asalnya  (2 * total) /100.......lepastu aku saja try buat formula math, eg "(12*15)/100".....die jadi error
        formatted_tax = '{0:.2f}'.format(tax) # guna ajaran gugel tukar format -> https://www.codegrepper.com/code-examples/python/frameworks/django/up+to+2+decimal+places+in+python
        grand_total = total + tax
        formatted_grand_total = '{0:.2f}'.format(grand_total) # tukar format ke 2 decimal point

    except ObjectDoesNotExist:
        pass #kalau object not exist/ x de apa2 berlaku tambahan barang dalam cart , dia just pass/ ignore je

    context = { #context= proses sending all the context/ data to HTML templete  #============================================== CONTEXT UPDATE KE HTML============================================================
        'total'                 : total,
        'quantity'              : quantity,
        'cart_items'            : cart_items,
        'tax'                   : tax,
        #'formatted_tax'         : formatted_tax, # untuk tukar format ke 2 decimal point
        'grand_total'           : grand_total,
        #'formatted_grand_total' : formatted_grand_total, # untuk tukar format ke 2 decimal point

    }
    return render(request, 'store/checkout.html', context)
