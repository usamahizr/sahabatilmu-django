from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from django.db.models import Q

from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None: #--------------------------BUTTON ALL CATEGORY ---------------------------------
        categories = get_object_or_404(Category, slug=category_slug) #katanya it will bring us the category
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id') #--------------------------ALL PRODUCT KAT STORE PAGE ---------------------------------
        paginator = Paginator(products, 3) # dalam " Paginator(product) " dia pass product yg ada kat atas tu "products = Product.objects.all().." ke paginator......6 tu jumlah produk yg akan muncul dalam STOIRE page
        page = request.GET.get('page') #capture URL that came with PAGE NUMBER....kalau bukak dekat link URL die tu, akan keluo ?page=2....itu yg bakal di GET kan
        paged_products = paginator.get_page(page) #asal 8 product, paged-product ni jumlah yg di filter kat paginator yg 6 tu,,,,paged product ni yg akan di pass ke templete
        product_count = products.count() #cara method python count jumlah product kat atas(LINE 6) untuk dia update kat STORE PAGE

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id= _cart_id(request), product=single_product).exists() # cart = foreign key untuk CartItem....boleh rujuk [=]models.py under[]carts.....so dia guna __ dalam "cart__cart_id" sebab dari cart dalam [=]models.py under[]carts  dia nak akses ke cat_id (ada kat line 8)

    except Exception as e:
        raise e

    context = {         #die konsep macam dictionary yg akan pass maklumat ke context under product_detail.html
        'single_product': single_product,
        'in_cart'       : in_cart,
    }
    return render(request, 'store/product_detail.html', context)

def search(request): #-------------------------- SEARCH FX ---------------------- ---------------------------------
    if 'keyword' in request.GET: # i) die cek GET request is keyword or not
        keyword = request.GET['keyword']    # ii)if ture we will store the value of keyword into kwyword variable
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))   # ".filter" nak search product yg ada keyword yg kita request tu tadi kat search area......"__icontains" it will look for the whole description and jika dia jumppa anything yg related dengan apa yg kita type tadi, dia akan bring that product
            product_count = products.count()
    context = {
        'products' : products,
        'product_count' : product_count,
    }
    return render(request, 'store/store.html', context)
